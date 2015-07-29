"""
log every file
and document when doing
data processing
"""

import csv


### CONFIG START ###

min_process_pct = 0.5
base_logger_path = '/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/logging/logs/' 
doc_logger_dir = base_logger_path + 'doc_logs/'
main_logger_path = base_logger_path + 'main_log.csv'

### CONFIG END ###



### PRE-PROCESSING ###


def setup_main_logger():
    """
    creates main logger
    handle, csv writer
    idempotently
    """
    main_logger_writer = open(main_logger_path,'w')
    main_logger_csv_writer = csv.DictWriter(main_logger_writer,main_logger_headers)
    return main_logger_writer, main_logger_csv_writer


def check_doc_logged(doc):
    """
    return log record
    if we have processed this doc
    according to log
    """
    if doc.file.name in files_logged:
        return [x for x in mail_logger_csv if x['file_name'] == doc.file.name][0]


def check_if_doc_processed(doc):
    """
    return boolean
    if file had minimum rows
    processed in last run
    """
    doc_log_record = check_doc_logged(doc)
    if doc_log_record:
        return doc_log_record['processed_pct'] > min_process_pct


def setup_doc_log(doc,mode):
    """
    create log for doc
    idempotently to show 
    processing details
    """
    return open(doc_logger_dir + doc.file.name.split('/')[-1],mode)


### MORE SET-UP ###


# only have to read in the main log once per run
main_logger_headers = [
                       'agency_name',
                       'attachment_id',
                       'file_name',
                       'file_type', # extension
                       'total_no_records',
                       'no_records_processed',
                       'no_invalid_records',
                       'pct_processed',
                       'header_found?',
                       'sample_last_name',
                       'sample_first_name',
                       'processed?',
                      ]

main_logger = open(main_logger_path,'r')
main_logger_writer, main_logger_csv_writer = setup_main_logger()
main_logger_csv = csv.DictReader(main_logger,main_logger_headers)
main_logger_csv = [x for x in main_logger_csv]

files_logged = [x['file_name'] for x in main_logger_csv]



### PROCESSING ###


def data_counts(attachment, csvdoc, agency_name, data, header):
    """
    return counts of things like 
    rows, processed, et cetera 
    in dict for writing
    """
    if len(data) > 1:
        sample_last_name = data[1]['last_name']
        sample_first_name = data[1]['first_name']
        data_bool = True
    else:
        sample_last_name = ''
        sample_first_name = ''
        data_bool = False
    #csvlist = [x for x in csvdoc]
    #if not csvlist:
    #    return
    try:
        row = {
               'agency_name': agency_name,
               'attachment_id': attachment.id,
               'file_name': attachment.file.name,
               'file_type': attachment.file.name.split('.')[-1],
               'total_no_records': len(csvdoc),
               'no_records_processed': len(data),
               'no_invalid_records': len(csvdoc) - len(data),
               #'no_invalid_records': len([x for x in csvdoc if x not in data]),
               'pct_processed': float(len(data)) / float(len(csvdoc)),
               'header_found?': header != None,
               'sample_last_name': sample_last_name,
               'sample_first_name': sample_first_name,
               'processed?': (float(len(data)) / float(len(csvdoc))) > min_process_pct,
              } 
        print row
        return row
    except Exception, e:
        print e # pass
        log_fail(agency_name,attachment,header,data_bool)

def log_fail(agency_name,attachment,header,data_bool):
    """
    things that don't get logged ...
    why does that shit happen here?
    we'll find out with this
    """
    fail_log = open('/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/logging/fail_log','a')
    fail_log_csv = csv.DictWriter(fail_log,['agency','attachment','header','data'])
    header_bool = header and True or False
    fail_log_csv.writerow({
                           'agency': agency_name,
                           'attachment': attachment.id,
                           'header': header_bool,
                           'data': data_bool
                          })
    fail_log.close()

def write_to_doc_log(doc_log, line):
    """
    writes the data from 
    data_counts() to a logger
    specific to doc
    """
    doc_log.write('|'.join(line))



### POST-PROCESSING ###

def write_to_main_log(attachment, csvdoc, agency_name, valid_data_log_path, headers, header): # args
    """
    return summary
    info about how this doc
    data was processed
    """
    print 'called write_to_main_log function'
    valid_data_log = open(valid_data_log_path,'r')
    csv_valid_data_log = csv.DictReader(valid_data_log,headers)
    print 'opened file for reading'
    # TODO: this segfaults on ISBE
    data = [x for x in csv_valid_data_log]
    print 'collected data in list'
    data = data_counts(attachment, csvdoc, agency_name, data, header)
    print 'obtained data_counts'
    if data:
        main_logger_csv_writer.writerow(data)

def sort_outfile_by_troublemaker():
    """
    convert csv
    to list then sort by processed,
    write to csv
    """
    outfile_reader = open(main_logger_path,'r')
    outfile_csv_reader = csv.DictReader(outfile_reader, main_logger_headers)
    outfile_list = [x for x in outfile_csv_reader]
    outfile_slist = sorted(outfile_list, key = lambda x: float(x['pct_processed']))
    outfile_reader.close()

    outfile_writer = open(main_logger_path,'w')
    outfile_csv_writer = csv.DictWriter(outfile_writer, main_logger_headers)
    outfile_csv_writer.writeheader()
    for row in outfile_slist:
        outfile_csv_writer.writerow(row)
    outfile_writer.close()
