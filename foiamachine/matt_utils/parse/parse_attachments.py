import csv, pprint
from apps.requests.models import *
from configs import *
from special_cases import * 
from validators import *
from logger import *
from transform import *
from meta import *
from formats import *

"""
test attachments:
379, 376 - straightforward csv


TODOS:
log invalid lines (except maybe blanks ...)
back this code up!!

"""



def init_parse(test=False):
    """
    kicks off file parsing
    writing data to output file;
    pass in list to test
    """
    outfile = open(outfile_file_path,'w')
    headers = ['attachment_id','processed_timestamp','agency', 'last_name', 'first_name', 'salary', 'title', 'department', 'start_date'] # TODO: don't repeat yourself
    outfile.write(','.join(headers) + '\n')
    outcsv = csv.DictWriter(outfile,headers)
    roll_through_atts(outcsv,test)


def roll_through_atts(outcsv,test):
    if test:
       attachments = [x for x in Attachment.objects.all() if x.id in test] # quality csv
    else:
       attachments = Attachment.objects.all()
    # need logic to handle multiple attachments/request
    for attachment in attachments:
       att_csv = csvify(attachment)
       if att_csv:
           print '#########'
           print 'attachment.id:', attachment.id
           print 'attachment.file.name:',attachment.file.name.encode()
           print '#########'
           data = roll_through_lines(att_csv, attachment)
           for row in data:
               outcsv.writerow(row)

def roll_through_lines(incsv, attachment):
    """
    come up with header
    ordering and roll through file 
    writing out data
    """
    
    data = [] # output
    header = None

    for line in iter(incsv):
        if header:
            row_data = check_data(header,line,attachment)
            if row_data: # skip invalid lines
                agency_name = None
                agency = get_attachment_agency(attachment)
                if agency:
                    agency_name = agency.name.encode()
                row_data = do_all_transformations(row_data, header, attachment)
                row_data['attachment_id'] = attachment.id
                row_data['agency'] = get_attachment_agency(attachment)
                row_data['processed_timestamp'] = now_str
                validated_row_data = validate_line(row_data)
                if validated_row_data:
                    data.append(validated_row_data)
                else:
                    log_invalid_line(row_data, attachment)
        else:
            header = check_header(line, attachment) # iterate til you find it
    pprint.pprint(data)
    return data
            


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
                        field_headers[header]['indices'].append(index)
            index += 1


        distinct_indices = [] # to avoid duplication
        # for now, first index is the best
        for field_header in field_headers:
            indices = field_headers[field_header]['indices']
            if indices:
                field_headers[field_header]['index'] = indices[0] # hack! TODO: fix or verify scalar
                if field_headers[field_header]['index'] in distinct_indices:
                    # indices shouldn't share between fields
                    # or we'll end up with duplication
                    return False
                else:
                    # this field is the only one using this index ... add to the list to prevent duplication
                    distinct_indices.append(field_headers[field_header]['index'])

        ambiguous_fields = [x for x in field_headers if len(field_headers[x]['indices']) > 1]
        if ambiguous_fields:
            print 'ambiguous:', ambiguous_fields
            # return False
            #TODO: figure this out later

        missed_requirements = [ x for x in field_headers if field_headers[x]['required'] and not field_headers[x]['indices']]
        if missed_requirements:
            return False
        return field_headers 


        # need a special rule for non-mutex keywords, i.e. first and last name
        # like if this header index is in multiple headers
            

def check_data(headers,line,attachment): 
    """
    return a dict of
    headers and field data joined
    by row's field index
    """
    row_data = dict((header,'') for header in headers) # fills in blank fields up front
    for header in headers:
        if headers[header]['indices']:
            index = headers[header]['indices'][0] # hack
            if index != None:
                if not line[index] and headers[header]['required']:
                    # required field is blank
                    return False
                row_data[header] = line[index]

    # row_data = validate_row(row_data,header)

    return row_data

def validate_data(row):
    return True 



def get_attachment_agency(attachment):
    for ma in attachment.message_attachments.all():
        if ma.request:
           return ma.request.agency
        for reply in ma.replies.all():
            if reply.request:
                return reply.request.agency

    return None



if __name__ == '__main__':
    init()
