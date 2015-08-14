import os, shutil
import hashlib
import csv
import datetime
from sets import Set
from pprint import pprint
from apps.requests.models import *
from apps.contacts.models import *
from apps.mail.models import *
from cleanup import *
from taggit.models import Tag
from bs4 import BeautifulSoup


# TODO: get atts with *no* requests and fix those using email body/sender

# att.file.name.split('.')[-1]
acceptable_extensions = ('xlsx','xls','xlsb','csv','txt','pdf','doc','docx')

response_report_filename = 'full_response_report.csv'

# don't count requests as missing attachments if they have these tags
exclusion_tags = ['no_employees', 'sort_out', 'postal_mail', 'test','inline_data']


def get_all_requests():
    """
    returns all requests  
    """
    return Request.objects.all()


def get_filtered_requests():
    """
    returns requests that
    aren't filtered by some kind of
    exclusion tagging
    """
    no_employees = Tag.objects.get(name='no_employees')
    return [r for r in get_all_requests() if no_employees not in r.tags.all()]

def get_all_attachments():
    return Attachment.objects.all()

def get_attachments_with_without_requests():
    atts_with_request = []
    atts_wo_request = []
    for att in get_all_attachments():
        request = None
        for ma in att.message_attachments.all():
            if ma.request:
                request = ma.request
            for rep in ma.replies.all():
                if rep.request:
                    request = rep.request
        if request:
            atts_with_request.append(att)
        else:
            atts_wo_request.append(att)
    return (atts_with_request, atts_wo_request)  


def is_attachment_acceptable(attachment):
    """
    returns boolean
    if attachment extension
    matches a whitelist  
    """
    return attachment.file.name.split('.')[-1].lower() in acceptable_extensions


def parent_orphaned_attachments(orphans=None,ymd_tuple=None):
    """
    for given list of 
    attachments, print info, set  
    agency ID
    """
    if not orphans:
        orphans = get_attachments_with_without_requests()[1]
    
    if ymd_tuple:
        y = ymd_tuple[0]
        m = ymd_tuple[1]
        d = ymd_tuple[2]
        cutoff = datetime.datetime(y,m,d)
        orphans = [x for x in orphans if x.created > cutoff]

    orphans = [x for x in orphans if is_attachment_acceptable(x)]

    for orphan in orphans:
        # TODO: find a way to remove dupes from this list
        mms = list(orphan.get_messages())
        if mms:
            for mm in mms:
                for k in mm.__dict__:
                    if k != 'body':
                        print k,':', mm.__dict__[k]
                print 'plain_text_body:'
                text = BeautifulSoup(mm.plain_text_body)
                pprint(text)
                
                print ""
                print "attachment.file.name", orphan.file.name
            if mms:
                agency_id = raw_input('agency_id...   ') 
            if agency_id:
                relate_att_to_agency(orphan,agency_id)


def parent_orphaned_messages(messages=None,agency_blob=None):
    """
    attachments without
    requests should get one tied to 
    given agency
    """

    if not messages:
        messages = Set([])
        for message in MailMessage.objects.all():
            if not message.request:
                for attachment in message.attachments.all():
                    if is_attachment_acceptable(attachment):
                        messages.add(message)

    if agency_blob:
        agencies = agency_blob.split('\n')
    else:
        agencies = [agency.name for agency in Agency.objects.all()]
    agency_messages = []
    for message in messages:
        for agency in agencies:
            if agency.lower() in message.body.lower():
                agency_messages.append(
                                       {'agency': Agency.objects.get(name=agency), 
                                        'message': message
                                       }
                                      )
    
    for agency_message in agency_messages:
        agency = agency_message['agency']
        message = agency_message['message']
        print ''
        print '================='
        print message.id
        print BeautifulSoup(message.plain_text_body)
        print [att.file.name for att in message.attachments.all()]
        prompt = 'Tie agency ' + agency.name + ', id ' +  str(agency.id) + ' to this message? [y/N]'
        tie = raw_input(prompt)
        if tie in ('y','Y'):
            if agency.request_set.all():
                request = agency.request_set.all()[0]
                message.request = request
                message.save()
            else:
                print agency.name, 'has no requests on file :/'



def print_alpha_agencies_ids():
    alpha_agencies = sorted([x for x in Agency.objects.all()], key = lambda x: x.name)
    for agency in alpha_agencies:
        print agency.id, agency.name


def relate_att_to_agency(att,agency_id):
    agency = Agency.objects.get(id=agency_id)
    requests = agency.request_set.all()
    if requests:
        request = requests[0]
    else:
        print ''
        print 'createing new request'
        print ''
        request = create_request(agency)
    rmms = list(request.mailmessage_set.all())
    if rmms:
        rmm = rmms[0]
    else:
        rmm = MailMessage.objects.get_or_create(request=request)[0]
    amm = att.get_messages()[0]
    rmm.replies.add(amm)
    rmm.save()
    request.save()
    if amm in rmm.replies.all() and request in agency.request_set.all():
        print 'assigning att.id', att.id, 'to request for', agency.name
    else:
        print 'fail'


def relate_msg_to_agency(msg_id,agency_id):
    msg = MailMessage.objects.get(id=msg_id)
    for att in msg.attachments.all():
        relate_att_to_agency(att,agency_id)


def old_parent_orphaned_attachments():
    """
    prompt for input,
    ID agency sending
    unrequested docs
    """
    atts_wo_requests = get_attachments_with_without_requests()[1]
    for att in atts_wo_requests:
        mas = att.message_attachments.all()
        if mas:
            ma = mas[0]
            if 'mkiefer' not in ma.email_from:
                email =  ma.email_from
            else:
                try:
                    email = ma.body.split('@')[1].split('"')[0]
                except:
                    email = 'this is too hard .......... att.id:', att.id
            message = 'email ' + str(email) + ' ... agency_id?' 
            agency_id = raw_input(message)
            if agency_id:
                # get the ID's agency's request
                agency = Agency.objects.get(id=agency_id)
                requests = agency.request_set.all()
                if requests:
                    request = requests[0]
                    #
                    rmm = list(request.mailmessage_set.all())[0] 
                    #
                    rmm.replies.add(ma)
                    rmm.save()
                    print 'assigning this attachment msg to request for', agency.name
            else:
                print 'no request found for agency'
        else:
            print 'no messages found for att.id', att.id


def get_all_agencies():
    """
    get all agencies
    to see who's in and who's out
    of the response list
    """
    all_agencies = sorted(list(Agency.objects.all()), key = lambda x: x.name)
    return [x for x in all_agencies if 'test' not in [y.name for y in x.tags.all()]]

def responding_agencies():
    """
    return a dict of
    respondents and deadbeats with
    status and contacts
    """
    agency_responses = {}
    for agency in get_all_agencies():
        name, attachments = check_agency_response(agency)
        agency_responses[name] = attachments
    return agency_responses
 

def get_request_tags(agency):
    if not list(agency.request_set.all()):
        print 'missing request:', agency.name
        return
    # what about agencies with multiple requests?
    all_tags = list(agency.request_set.all()[0].tags.all())
    return [x for x in all_tags if x.name in exclusion_tags]


def check_agency_response(agency):
    """
    returns agency, list
    of attachments if any
    
    """
    attachments = []
    tags = get_request_tags(agency)
    if tags:
        for tag in tags:
            attachments.append(tag.name)
    for req in agency.request_set.all():
        for mm in req.mailmessage_set.all():
            for att in mm.attachments.all():
                if is_attachment_acceptable(att):
                    attachments.append(att)
            for rep in mm.replies.all():
                for att in rep.attachments.all():
                    if is_attachment_acceptable(att):
                        attachments.append(att)
    return (agency.name.encode(), attachments)


def report():
    agencies_responses = [check_agency_response(x) for x in get_all_agencies()]
    agencies_with_atts = [x for x in agencies_responses if x[1]]
    agencies_without_atts = [x for x in agencies_responses if not x[1]]    
    #print 'attachment count:', len(list(get_all_attachments()))
    #print 'agency count:', len(list(get_all_agencies()))
    print 'total agency count:', len(agencies_responses)
    print 'agencies responded count:', len(agencies_with_atts)
    print 'agencies not responded count:', len(agencies_without_atts)
    pprint(responding_agencies())


def identify_blank_agencies():
    """
    Attachments with blank
    agencies will print
    alongside email
    """
    requests = {}
    for att in Attachment.objects.all():
        for ma in att.message_attachments.all():
            for rep in ma.replies.all():
                if rep.request:
                    request = rep.request
                    request_meta = {}
                    request_meta['request'] = request
                    request_meta['emails'] = []
                    if request.agency_id in (21,452): # empty string agency:
                        for con in request.contacts.all():
                            for email in con.emails.all():
                                request_meta['emails'].append(email.get_email.encode())
                        requests[request.id]=request_meta    


    for reqid in requests:
        request_meta = requests[reqid]
        request = request_meta['request']
        if request_meta['emails']:
            msg = 'Please enter agency id ...\n'
            msg += ','.join(request_meta['emails'])
            msg += '\n\n\n\n'
            aid = raw_input(msg)

            if aid:
                agency = Agency.objects.get(id=aid)
                request.agency_id = aid
                government = Government.objects.get(name=agency.name)
                request.government_id = government.id
                contacts = request.contacts.all()
                for contact in contacts:
                    contact.set_new_agency(agency)
                print 'Updating request id', reqid 
                print 'contact emails', request_meta['emails'], 'with', Agency.objects.get(id=aid).name.encode()
                print 'new request.agency, contacts.agency ->', agency.id, agency.name
                print 'new request.government', government.id, government.name
                request.save()

def get_file_extension(attachment):
    return attachment.file.name.encode().split('.')[-1]

def get_file_name(attachment):
    return attachment.file.name.encode()[61:] #hack based on att path

def get_request_attachments():
    """
    return tuple of
    (request id, attachments)
    to see who's in, out
    """
    requests = Request.objects.all()
    request_atts = []
    for request in requests:
        atts = Set([])
        for mm in request.mailmessage_set.all():
            for rep in mm.replies.all():
                for att in rep.attachments.all():
                    atts.add(att)
        request_atts.append((request.id,atts)) 
    return request_atts


def unsent_report():
    """
    return agencies
    that didn't get a request
    based on messages
    """

    unsent_agencies = []

    all_tos = Set([])
    for mm in MailMessage.objects.all():
        for to in mm.to.all():
            if len(to.content.split('@')) > 1:
                all_tos.add(to.content.split('@')[1])

    for agency in Agency.objects.all():
        agency_messages = []
        for contact in agency.contacts.all():
            for email in contact.emails.all():
                 if email.content.split('@')[1] in all_tos:
                     agency_messages.append(email)
        if not agency_messages:
            unsent_agencies.append(agency)
    
    return unsent_agencies 



def full_report():
    """
    everything you need
    to know to hunt down deadbeats
    in a csv
    """
    with open(response_report_filename,'w') as outfile:
        headers = [
                   "agency_name",  
                   "attachments_count", 
                   "processed",   
                   "contacts",
                   "submitted_by?",
                   "request_id",
                   "agency_id",
                   "attachment_ids"
                  ]
        outcsv = csv.DictWriter(outfile,headers)
        outcsv.writeheader()

        agency_responses = responding_agencies() # {agency:[attachments]}

        for agency in agency_responses:
            try:
                # duplicate agency names should be reported
                agency = Agency.objects.get(name=agency)
            except Exception, e:
                print agency, e
                continue

            emails = []
            for contact in agency.contacts.all():
                [emails.append(email.content) for email in contact.emails.all()]

            row = {
                   'agency_name'           : agency.name,
                   'attachments_count'     : len(agency_responses[agency.name]),
                   'processed'             : 'TBD', # need some better logging
                   'contacts'              : ','.join([email.encode('utf-8') for email in emails]),
                   'submitted_by?'         : '', # report user fills out 
                   'request_id'            : ','.join([str(request.id) for request in agency.request_set.all()]),
                   'agency_id'             : agency.id,
                   'attachment_ids'        : ','.join([str(attachment.id) for attachment in agency_responses[agency.name]]),
                  }
            try:
                outcsv.writerow(row)
            except Exception, e:
                print e
                pprint(row) # report problems


def update_response_report(path_to_existing):
    """
    update attachment
    counts for each agency while
    keeping notes and stuff
    """
    # get the existing report
    existing_report = open(path_to_existing)
    raw_existing_headers = existing_report.next().split(',')
    existing_headers = []
    for x in raw_existing_headers:
        x = x.replace('\n','')
        x = x.replace('\r','')
        existing_headers.append(x)
    existing_report_csv = list(csv.DictReader(existing_report,existing_headers))

    # get the new report
    new_report = open(response_report_filename)
    raw_new_headers = new_report.next().split(',')
    new_headers = []
    for x in raw_new_headers:
        x = x.replace('\n','')
        x = x.replace('\r','')
        new_headers.append(x)
    new_report_csv = list(csv.DictReader(new_report, new_headers)) 
    
    # prepare updated report
    updated_path = 'updated_' + path_to_existing
    updated_report = open(updated_path,'w')
    updated_headers = existing_headers
    updated_report.write(','.join(updated_headers) + '\n')
    updated_report_csv = csv.DictWriter(updated_report, updated_headers)

    for row in existing_report_csv:
        # get each agency's corresponding rows for old and new reports
        matching_agency_rows = [x for x in new_report_csv if x['agency_name'] == row['agency_name']] # fuck. hack
        if len(matching_agency_rows) == 1:
            new_report_row = matching_agency_rows[0]
        else:
            print 'scalar not returned for ', row['agency_name'], ';', len(matching_agency_rows), 'results found instead'
            continue
        row['attachments_count'] = new_report_row['attachments_count']
        row['attachment_ids'] = new_report_row['attachment_ids'] # '\r\n'
        row['request_id'] = new_report_row['request_id']
        updated_report_csv.writerow(row)

    updated_report.close()


def old_update_response_report(path_to_file):
    """
    update attachment
    counts for each agency while
    keeping notes and stuff
    """
    # get data from old csv as list of row dicts
    infile = open(path_to_file,'r')
    headers = infile.next().split(',')
    full_report = open(response_report_filename,'r')
    raw_report_headers = [x for x in full_report.next().split(',')]
    full_report_headers = []
    for x in raw_report_headers:
        x = x.replace('\n','')
        x = x.replace('\r','')
        full_report_headers.append(x)
    
    # TODO fix crazy header stuff
    incsv = csv.DictReader(infile,full_report_headers)
    incsv = list(incsv)
    infile.close()

    # run a new response report
    # full_report() # variable referenced before assignment??
    full_report_csv = csv.DictReader(full_report, full_report_headers)
    full_report_csv = list(full_report_csv)

    # overwriting the old file
    outfile = open(path_to_file,'w')
    outcsv = csv.DictWriter(outfile,full_report_headers)
    outcsv.writeheader()

    for row in incsv:
        # get each agency's corresponding rows for old and new reports
        matching_agency_rows = [x for x in full_report_csv if x['agency_name'] == row['agency_name']]
        if len(matching_agency_rows) == 1:
            new_report_row = matching_agency_rows[0]
        else:
            import pdb; pdb.set_trace()
            print 'scalar not returned for ', row['agency_name'], ';', len(matching_agency_rows), 'results found instead'
            continue
        row['attachments_count'] = new_report_row['attachments_count']
        import pdb; pdb.set_trace()
        row['attachment_ids']
        new_report_row['attachment_ids'] # '\r\n'
        row['request_id'] = new_report_row['request_id']
        outcsv.writerow(row)

    outfile.close()


def attachment_report():
    """
    deliverable
    report of file attachments
    grouped by agency
    """
    agency_att_dir = 'Payroll_FOIA_attachments'
    # idemopotency
    if os.path.exists(agency_att_dir):
        shutil.rmtree(agency_att_dir)
    os.mkdir(agency_att_dir)
    
    for agency in get_all_agencies():
        if agency.name:
            # set up a directory for each agency
            agency_name = clean_name(agency.name)
            agency_dir = agency_att_dir + '/' + agency_name
            os.mkdir(agency_dir)
            notes_file = open(agency_dir + '/' + agency_name + ' notes.txt','w')

            # de-duplication via checksum
            hashes = []
            attachments = []
            for att in check_agency_response(agency)[1]:
                if type(att) == Attachment: # filters out unicode tags
                    att_hash = hashlib.md5(open(att.file.path).read())
                    if att_hash in hashes:
                        print 'skipping dupe hash:', att.file.name, att_hash
                        continue
                    attachments.append(att)
                    hashes.append(att_hash)
                else: # write tags to notes file
                    notes_file.write(att)
            if agency_name.lower() == 'barrington': import pdb; pdb.set_trace()    
            notes_file.close()

            for att in attachments:
                shutil.copy(att.file.path,agency_dir) # copy the attachment here
                # print 'copying', att.file.path, 'to', agency_dir


def pdfs_suck():
    """
    writes report with
    list of agencies who just 
    gave us pdfs
    """
    headers = ['agency', 'request_id', 'file_attachments'] 
    outfile = open('pdfs_suck.csv','w')
    outcsv = csv.DictWriter(outfile, headers)
    outfile.write(','.join(headers) + '\n')
    for ra in pdfs_only():
        outcsv.writerow(row)
    outfile.close()


def pdfs_only():
    return [ ra for ra in get_request_attachments() if is_pdf_only(ra)]


def is_pdf_only(ra):
    """
    returns requests with
    pdfs, but no spreadsheet
    to id, log and fix
    """
    spreadsheet = False
    pdf = False
    atts = ra[1]
    for att in atts:
        ext = att.file.name.split('.')[-1]
        if ext in ('xls', 'xlsx', 'csv'):
            spreadsheet = True
        if ext in ('pdf'):
            pdf = True
    if atts and pdf and not spreadsheet:
        request = None
        for ma in att.message_attachments.all():
            if ma.request:
                request = ma.request
            for rep in ma.replies.all():
                if rep.request:
                    request = rep.request
        if request:
            row = {
                    'agency': request.agency.name, 
                    'request_id': request.id, 
                    'file_attachments': [x.file.name.split('/')[-1] for x in
                    atts if x.file.name.split('.')[-1] == 'pdf']
                  }
            
            # not validated!
            return row



def clean_name(name):
    return name.replace('/','-')


def new_request(agency_name,req_id=1):
    from apps.government.utils import get_defaults, get_or_create_us_govt
    req = Request.objects.get(id=req_id)    
    me = User.objects.get(username='matthewlkiefer')
    govt = get_or_create_us_govt(agency_name,'city')
    agency, created = Agency.objects.get_or_create(name=agency_name,government=govt)
    contact, created = Contact.objects.get_or_create(first_name='FOIA Officer', last_name=agency_name)
    request = Request.objects.create(
                            author_id= me.id, 
                            government_id = govt.id, 
                            agency_id = agency.id, 
                            text = req.text, 
                            free_edit_body = req.free_edit_body, 
                            title = req.title
              )   
    request.contacts.add(contact)
    request.save()

# TODO: tool to join messages with requests (for manual forwards from gmail ... look up thread id somewhere ... start from all attachments) - 1 hr

# TODO: report contacts of agencies that didn't submit (easy) - 0.5 hr

# TODO: auto-send to agencies that didn't submit (crib off old script) - 0.5 hr 

