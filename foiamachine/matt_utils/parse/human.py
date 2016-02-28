from csvkit import DictReader
from csvkit.utilities.in2csv import In2CSV
from csvkit.utilities.csvlook import CSVLook
import StringIO

from apps.requests.models import Attachment
#from logging.logger import main_logger_path
#from parse_attachments import get_attachment_agency
from formats import listify

from matt_utils.parse.parse_attachments import get_attachment_agency, get_attachment_request
from matt_utils.parse.formats import tabula_csv
from matt_utils.parse.special_cases import cases

special_case_ids = [x['attachment_id'] for x in cases]

default_head_n = 10

def human_header(test=None, head_n=None):
    if not head_n:
        head_n = default_head_n
    if test:
        # weird to note that the following list comp does not preserve order:
        # atts = [x for x in Attachment.objects.all() if x.id in test]# and x.id not in special_case_ids]
        atts = []
        for x in test:
            atts.append(Attachment.objects.get(id=x))
        att_ids = [x.id for x in atts]
        print 'test = ', [x.id for x in atts]
        print 'att id lookup failed', [x for x in test if x not in att_ids] 
    else:
        atts = read_log()
    for attachment in atts:
        print 'trying attachment id', attachment.id
        print 'url:', 'bettergov.info' + attachment.get_public_url
        try:
            data = convert_attachment(attachment)
            #data = listify(attachment)
            if data:
                head_data(attachment, data, head_n)
            else:
                print 'no data ... convert_attachment() failed'
        except Exception, e:
            print '****'
            print 'error convering attachment id', attachment.id
            print e
            print '****'
        raw_input('')


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
    ext = outfile_path.split('.')[-1].lower()
    if ext not in ('xls', 'xlsx', 'csv','pdf'):
        return
    infile_path = attachment.file.path
    if ext == 'pdf':
        infile_path = tabula_csv(attachment,listify = False)
    # in2csv ... can't say the python module utlities are working 100% here
    #convert = In2CSV(args=[attachment.file.path], output_file=outfile) 
    #convert.main()
    import subprocess
    print 'attachment_id = ', attachment.id
    print 'agency = ', get_attachment_agency(attachment)
    print 'infile_path = ',infile_path
    if ext == 'csv':
        # already csv
        outfile_path = infile_path
    else:
        subprocess.call(['in2csv',
            #'--format',outfile_path.split('.')[-1].lower(),
            infile_path], #attachment.file.path],
            stdout=outfile)
    # label column headers by zero-index
    headers = get_headers(outfile_path)
    if headers:
        write_header_indices(outfile_path, headers)
        # csvlook file | head
        output = StringIO.StringIO()
        look = CSVLook(args=[outfile_path, '-l'], output_file=output)
        look.main()

        input = StringIO.StringIO(output.getvalue()) 
        return input
    else:
        print 'something wrong with headers. attachment id', attachment.id


def head_data(attachment, input, head_n):
    """
    as in head -n x
    """
    #import ipdb; ipdb.set_trace()
    agency = get_attachment_agency(attachment)
    request = get_attachment_request(attachment)
    #agency_name = agency and agency.name or 'none'
    print '##################'
    print 'attachment id:      ', attachment.id
    print 'attachment filename:', attachment.file.name
    print 'agency:             ', agency.name
    #print 'request:            ', request.id
    print '##################'
    line = 0
    if type(input) == list:
        for x in input:
            print x
            line += 1
            if line == head_n:
                break
    else:
        while line < head_n:
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
    readfile = open(path,'r')
    dreader = DictReader(readfile)
    fieldnames = dreader.fieldnames
    if not fieldnames:
        import ipdb; ipdb.set_trace()
    readfile.close()
    return fieldnames

def write_header_indices(path,header):
    """
    write zero-indexed headers to file
    """
    rf = open(path,'r')
    data = [x for x in rf]
    rf.close()
    wf = open(path,'w')
    # prepend headers with index numbers
    wf.write('"' + '","'.join([str(x) + ' - ' + header[x] for x in range(0, len(header))]) + '"\n')
    # skip the header cuz we rewrote it
    for x in data[1:]:
        wf.write(x)
    wf.close()
