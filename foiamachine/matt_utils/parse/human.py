from csvkit import DictReader
from csvkit.utilities.in2csv import In2CSV
from csvkit.utilities.csvlook import CSVLook
import StringIO

from apps.requests.models import Attachment
#from logging.logger import main_logger_path
#from parse_attachments import get_attachment_agency


def human_header(test=None):
    if test:
        atts = [x for x in Attachment.objects.all() if x.id in test]
    else:
        atts = read_log()
    for attachment in atts:
        data = convert_attachment(attachment)
        if data:
            head_data(attachment, data)
            

def read_log():
    atts = []
    # read parse_attachments.init_parse() log
    # with open(main_logger_path,'r') as log:
    log = open('/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/logging/logs/main_log.csv','r')
    #import ipdb; ipdb.set_trace()
    logcsv = DictReader(log)
    for row in logcsv:    
        #logcsv = DictReader(log)
        #for row in logcsv:
        # look at header-less files
        if row['header_found?'] != 'True':
            atts.append(Attachment.objects.get(id=str(row['attachment_id'])))
    return atts
 

def convert_attachment(attachment):
    outfile_path = '/tmp/'+attachment.file.name.split('/')[-1]
    outfile = open(outfile_path,'w')
    # in2csv
    convert = In2CSV(args=[attachment.file.path], output_file=outfile) 
    convert.main()
    # label column headers by zero-index
    headers = get_headers(outfile_path)
    if headers:
        return
        write_header_indices(outfile_path, headers)
        # csvlook file | head
        output = StringIO.StringIO()
        look = CSVLook(args=[outfile_path, '-l'], output_file=output)
        look.main()

        input = StringIO.StringIO(output.getvalue()) 
        return input
    else:
        print 'something wrong with headers. attachment id', attachment.id


def head_data(attachment, input):
    """
    as in head -n x
    """
    #import ipdb; ipdb.set_trace()
    # agency = get_attachment_agency(attachment)
    #agency_name = agency and agency.name or 'none'
    print '##################'
    print 'attachment id:', attachment.id
    # print 'agency:', agency.name
    print '##################'
    line = 0
    while line < 50:
        print input.next()
        line += 1
    raw_input('')
    for x in range(0,5):
        print ''
    
    # do yo thang:
    # code fix 
    # or
    # special case


def get_headers(path):
    f = open(path,'r')
    c = DictReader(f)
    l = c.fieldnames
    f.close()
    return l

def write_header_indices(path,header):
    """
    write zero-indexed headers to file
    """
    rf = open(path,'r')
    data = [x for x in rf]
    rf.close()
    wf = open(path,'w')
    # prepend headers with index numbers
    wf.write(','.join([str(x) + ' - ' + header[x] for x in range(0, len(header) - 1)]) + '\n')
    # skip the header cuz we rewrote it
    for x in data[1:]:
        wf.write(x)
    wf.close()
