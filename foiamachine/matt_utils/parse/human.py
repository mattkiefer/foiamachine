from csvkit import DictReader
from csvkit.utilities.in2csv import In2CSV
from csvkit.utilities.csvlook import CSVLook
import StringIO

from apps.requests.models import Attachment
from logging.logger import main_logger_path


def human_header():
    # read parse_attachments.init_parse() log
    with open(main_logger_path,'r') as log:
        logcsv = DictReader(log)
        for row in logcsv:
            # look at header-less files
            if row['header_found'] != 'True':
                attachment = Attachment.objects.get(id=str(row['attachment_id']))
                # in2csv file
                outfile_path = '/tmp/'+attachment.file.name
                In2CSV(args=[attachment.file.path], output_file=outfile_path) 
                # csvlook file | head
                output = StringIO.StringIO()
                look = CSVLook(args=[outfile_path], output)
                look.main()

                input = StringIO.StringIO(output.getvalue()) 
                line = 0
                while line < 10:
                    print input.next()
                    line += 1
                raw_input('')
                
                # do yo thang:
                # code fix 
                # or
                # special case
