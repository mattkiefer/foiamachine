
mxs = []
for x in MailMessage.objects.all():
    

mxs = [ x for x in MailMessage.objects.all() if not x.request and x.attachments.all()]


