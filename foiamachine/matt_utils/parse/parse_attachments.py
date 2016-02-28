import csv, pprint
from apps.requests.models import *
from configs import *
from special_cases import * 
from validators import *
from logging.logger import *
from transform import *
from meta import *
from formats import *
from get_attachments import get_deduped_attachments
from matt_utils.logging.log_checker import get_processed_attachment_ids

"""
test attachments:
379, 376 - straightforward csv


TODOS:
log invalid lines (except maybe blanks ...)

"""

valid_data_log_path = '/tmp/valid_data_log.tmp'
processed_agencies_path = '/home/ubuntu/foiamachine/repo/foiamachine/output_data/processed_agencies.txt'
processed_agencies = { x.rstrip() for x in open(processed_agencies_path)}
headers = ['attachment_id','processed_timestamp','agency', 'last_name', 'first_name', 'salary', 'title', 'department', 'start_date']
fail_limit = 1000 # for giving up on long files missing EOL
test_fail_limit = 1000 


def init_parse(test=False):
    """
    kicks off file parsing
    writing data to output file;
    pass in list to test
    """
    outfile = open(outfile_file_path,'w')
    outfile.write(','.join(headers) + '\n')
    outfile.close()
    roll_through_atts(test)
    main_logger_writer.close()
    sort_outfile_by_troublemaker()



def roll_through_atts(test):
    """
    get each attachment
    then turn into csv,
    parse lines, write data
    """
    if test:
        attachments = [x for x in Attachment.objects.all() if x.id in test]
    else:
        attachments = get_deduped_attachments()
        attachments = [x for x in attachments if x.id not in get_processed_attachment_ids()]
    # TODO: figure out why attachments isn't returning ids [208, 243, 892, 975]
    for attachment in attachments:
        print '#########'
        print 'attachment.id:', attachment.id
        print 'attachment.file.name:',attachment.file.name.encode()
        print '#########'
       
        if (skip(attachment) or processed(attachment) or is_request_deleted(attachment)):
            print '*** skipping ***'
            import ipdb; ipdb.set_trace()
            continue
        att_list = listify(attachment)
        if att_list:
            # logging happens here
            roll_through_lines(att_list, attachment, test)
            #raw_input('')


def roll_through_lines(att_list, attachment, test):
    """
    come up with header
    ordering and roll through file 
    writing out data
    """
    data = [] # output
    header = None
    processed = False

    # clear the doc log
    doc_log = setup_doc_log(attachment,'w')
    doc_log.write('')
    doc_log.close()
    agency_name = None
    agency = get_attachment_agency(attachment)
    if agency:
        agency_name = agency.name.encode()
    valid_data_log = open(valid_data_log_path,'w')
    valid_data_log.write(','.join(headers) + '\n')
    valid_data_log.close()
    #
    # includes logic to pass if this data was already processed,
    # logging at the file level in the main log,
    # and logging at the row level for this attachment's data
    #
    
    consecutive_fail = 0
    for line in att_list:
        
        #if attachment.id == 507:
        #    counter +=1 
        #    print counter
        valid = False
        if header and line:
            # validation
            row_data = check_data(header,line)
            if row_data: # skip invalid lines
                row_data = do_all_transformations(row_data, header, attachment)
                row_data['attachment_id'] = attachment.id
                row_data['agency'] = get_attachment_agency(attachment)
                row_data['processed_timestamp'] = now_str
                validated_row_data = validate_line(row_data)
                #import pdb; pdb.set_trace()
                if validated_row_data:
                    valid = True
                    # utf-8 output
                    validated_row_data['agency'] = validated_row_data['agency'].name
                    validated_row_data['attachment_id'] = str(validated_row_data['attachment_id'])
                    validated_row_data['salary'] = str(validated_row_data['salary'])
                    try:
                        utf8_validated_row_data = {}
                        for x in validated_row_data:
                            utf8_validated_row_data[x] = validated_row_data[x].decode('utf-8').encode('utf-8')
                        # validated_row_data = dict((x, validated_row_data[x].encode('utf-8')) for x in validated_row_data)   
                    except Exception, e:
                        print e
                        continue
                        import ipdb; ipdb.set_trace()
                    consecutive_fail = 0
                    #data.append(validated_row_data)
                    # for logging
                    # ... why bother
                    try:
                        valid_data_log = open(valid_data_log_path,'a')
                        csv_valid_data_log = csv.DictWriter(valid_data_log, headers)
                        csv_valid_data_log.writerow(validated_row_data)
                        valid_data_log.close()
                    except:
                        print 'valid data logging failed ***(&(&^#%@)*%@%'
                    # for data output
                    outfile = open(outfile_file_path,'a')
                    outcsv = csv.DictWriter(outfile,headers)
                    outcsv.writerow(utf8_validated_row_data)
                    outfile.close()
                    # we passed validation and wrote data ... put this agency down as processed so we don't rerun
                    processed = True
        else:
            # iterate until you find header
            header = check_header(line, attachment)
            if header:
                print 'header .....................'
                import pprint; pprint.pprint(header)
                valid = True
                consecutive_fail = 0
        if not valid:
            # log stuff that's not a header or data
            doc_log = setup_doc_log(attachment,'a')
            write_to_doc_log(doc_log,line)
            doc_log.close()
            consecutive_fail += 1
            print 'consecutive fail', consecutive_fail
            if test:
                fail_limit = test_fail_limit
            else: # hack! TODO: fix
                fail_limit = 1000
            if consecutive_fail == fail_limit:
                print 'too many consecutive fails ... continuing'
                break


    # log how this doc processed overall
    write_to_main_log(attachment, att_list, agency_name, valid_data_log_path, headers, header)

    # add this agency to file so we don't rerun it
    if processed:
        mark_as_processed(utf8_validated_row_data['agency'])

            

def check_header(line, attachment):
    """
    returns header row
    or False
    """
    field_headers = get_field_headers()
    index = 0 # offset for columns
    
    # is this doc a special case?
    special = check_if_special(attachment.id, field_headers, cases)
    if special:
        print 'special case'
        return special # field_headers populated with special indices
    else: # collect indices manually ... should break this fxn up    
        for field in line:
            for header in field_headers:
                for keyword in field_headers[header]['keywords']:
                    if keyword in field.lower():
                        field_headers[header]['indices'].add(index)
            index += 1
        
        # TODO: straighten out when 'name' is in first and last name fields
        distinct_indices = [] # to avoid duplication
        # for now, first index is the best
        for field_header in field_headers:
            indices = field_headers[field_header]['indices']
            if indices:
                field_headers[field_header]['index'] = list(indices)[0] # hack! TODO: fix or verify scalar
                field_headers = disambiguate_first_and_last(field_headers)
                this_index = field_headers[field_header]['index']
                if this_index in distinct_indices:
                    # indices shouldn't share between fields
                    # or we'll end up with duplication
                    print '** multiple fields claiming the same indices:',  [x for x in field_headers if this_index in field_headers[x]['indices']]
                    print field_headers
                    return None
                else:
                    # this field is the only one using this index ... add to the list to prevent duplication
                    distinct_indices.append(field_headers[field_header]['index'])
        #import pdb; pdb.set_trace()
        ambiguous_fields = [x for x in field_headers if len(field_headers[x]['indices']) > 1]
        if ambiguous_fields:
            #import ipdb; ipdb.set_trace()
            print 'ambiguous:', ambiguous_fields
            # return False
            #TODO: figure this out later

        missed_requirements = [ x for x in field_headers if field_headers[x]['required'] and not field_headers[x]['indices']]
        if missed_requirements:
            print 'missed_requirements:', missed_requirements
            return None
        # data_row = disambiguate_first_and_last(data_row)
        return field_headers 



        # need a special rule for non-mutex keywords, i.e. first and last name
        # like if this header index is in multiple headers
            

def check_data(headers,line): 
    """
    return a dict of
    headers and field data joined
    by row's field index
    """
    row_data = dict((header,'') for header in headers) # fills in blank fields up front
    for header in headers:
        if headers[header]['indices']:
            index = list(headers[header]['indices'])[0] # hack
            if index != None:
                try:
                    if not line[index] and headers[header]['required']:
                        # required field is blank
                        return False
                    row_data[header] = line[index]
                except:
                    pass
    # row_data = validate_row(row_data,header)

    return row_data


def get_attachment_agency(attachment):
    """
    look up agency
    to label row as such in
    final export file
    """
    for ma in attachment.message_attachments.all():
        if ma.request:
            return ma.request.agency
        for reply in ma.replies.all():
            if reply.request and reply.request.agency and reply.request.agency.name:
                return reply.request.agency
    print 'None'
    return None


def is_request_deleted(attachment):
    """
    attachments process
    only if their requests are
    not marked deleted
    """
    request = get_attachment_request(attachment)
    if request:
        return request.status in ('X')
    else:
        return True

def get_attachment_request(attachment):
    """
    look up request to 
    check if should be deleted
    among other things
    """
    for ma in attachment.message_attachments.all():
        if ma.request:
           return ma.request
        for reply in ma.replies.all():
            if reply.request:
                return reply.request
    return None



def parse_pdfs():
    from matt_utils.responses.response_report import pdfs_only
    pdfs = []
    for req_atts in pdfs_only():
        for att in req_atts[1]:
            if att.file.name.split('.')[-1] == 'pdf':
                pdfs.append(att.id)
    init_parse(test=pdfs) 


def processed(attachment):
    return False #get_attachment_agency(attachment).name in processed_agencies 


def mark_as_processed(agency):
    # check if this agency is already in the processed list
    if agency not in processed_agencies:
        # if not, append to in-memory set AND file
        # 2nd thought: maybe don't add this to set because there could be multiple files in a run
        # processed_agencies.add(agency)
        processed_agencies_file_a = open(processed_agencies_path,'a')
        processed_agencies_file_a.write(agency + '\n')
        processed_agencies_file_a.close()
        

if __name__ == '__main__':
    init()
