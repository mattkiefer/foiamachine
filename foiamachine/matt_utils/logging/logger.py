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
    main_logger_csv_writer.writeheader()
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


def setup_doc_log(doc):
    """
    create log for doc
    idempotently to show 
    processing details
    """
    return open(doc_logger_dir + doc.file.name.split('/')[-1],'w')


### MORE SET-UP ###


# only have to read in the main log once per run
main_logger_headers = [
                       'agency_name',
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
    if data:
        sample_last_name = data[0]['last_name']
        sample_first_name = data[0]['first_name']
    else:
        sample_last_name = ''
        sample_first_name = ''
    try:
        return {
            'agency_name': agency_name,
            'file_name': attachment.file.name,
            'file_type': attachment.file.name.split('.')[-1],
            'total_no_records': len(csvdoc),
            'no_records_processed': len(data),
            'no_invalid_records': len([x for x in csvdoc if x not in data]),
            'pct_processed': float(len(data)) / float(len(csvdoc)),
            'header_found?': header != None,
            'sample_last_name': sample_last_name,
            'sample_first_name': sample_first_name,
            'processed?': (float(len(data)) / float(len(csvdoc))) > min_process_pct,
            } 
    except Exception, e:
        import pdb; pdb.set_trace()


def write_to_doc_log(doc_log, line):
    """
    writes the data from 
    data_counts() to a logger
    specific to doc
    """
    doc_log.write('|'.join(line))



### POST-PROCESSING ###

def write_to_main_log(attachment, csvdoc, agency_name, data, header): # args
    """
    return summary
    info about how this doc
    data was processed
    """
    data = data_counts(attachment, csvdoc, agency_name, data, header)
    main_logger_csv_writer.writerow(data)
