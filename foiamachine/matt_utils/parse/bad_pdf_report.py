import os
from apps.requests.models import *

atts = Attachment.objects.all()

pdfs = [x for x in atts if '.pdf' in x.file.name]

for pdf in pdfs:
    path = pdf.file.path.replace(' ','\ ').replace('(','\(').replace(')','\)')
    com = 'pdftotext -layout ' + path + ' tmp.txt'
    # print com
    os.system(com)
    tmp_file = open('tmp.txt','r')
    if len(tmp_file.read()) <= 100:
        if list(pdf.message_attachments.all()) and pdf.message_attachments.all()[0].request:
            print pdf.message_attachments.all()[0].request.agency.name
    else:
        pass #print 'lines', path
    tmp_file.close()
