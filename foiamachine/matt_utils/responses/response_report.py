import csv
from sets import Set
from pprint import pprint
from apps.requests.models import *
from apps.contacts.models import *
from apps.mail.models import *
from cleanup import *
from taggit.models import Tag


# TODO: get atts with *no* requests and fix those using email body/sender

# last 4
acceptable_extensions = ('xlsx','.xls','.csv','.txt','.pdf')

response_report_filename = 'full_response_report.csv'


def get_all_attachments():
    """
    returns all attachments
    """
    return Attachment.objects.all()


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


def parent_orphaned_attachments(orphans=None):
    """
    for given list of 
    attachments, print info, set  
    agency ID
    """
    if not orphans:
        orphans = get_attachments_with_without_requests()[1]
    for orphan in orphans:
        # TODO: find a way to remove dupes from this list
        mms = list(orphan.get_messages())
        if mms:
            for mm in mms:
                pprint(mm.__dict__)
                print ""
                print "attachment.file.name", orphan.file.name
            if mms:
                agency_id = raw_input('agency_id...   ') 
            if agency_id:
                relate_att_to_agency(orphan,agency_id)


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
    return sorted(list(Agency.objects.all()), key = lambda x: x.name)


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
        
     
def check_agency_response(agency):
    """
    returns agency, list
    of attachments if any
    
    """
    attachments = []
    for req in agency.request_set.all():
        for mm in req.mailmessage_set.all():
            for rep in mm.replies.all():
                for att in rep.attachments.all():
                    if att.file.name[-4:].lower() in acceptable_extensions:
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
    from sets import Set

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


def update_response_report(path_to_file):
    """
    update attachment
    counts for each agency while
    keeping notes and stuff
    """
    # get data from old csv as list of row dicts
    infile = open(path_to_file,'r')
    headers = infile.next().split(',')
    incsv = csv.DictReader(infile,headers)
    incsv = list(incsv)
    infile.close()

    # run a new response report
    # full_report() # variable referenced before assignment??
    full_report = open(response_report_filename,'r')
    full_report_headers = full_report.next().split(',')
    full_report_csv = csv.DictReader(full_report, full_report_headers)
    full_report_csv = list(full_report_csv)

    # overwriting the old file
    outfile = open(path_to_file,'w')
    outcsv = csv.DictWriter(outfile,headers)
    outcsv.writeheader()

    for row in incsv:
        # get each agency's corresponding rows for old and new reports
        matching_agency_rows = [x for x in full_report_csv if x['agency_name'] == row['agency_name']]
        if len(matching_agency_rows) == 1:
            new_report_row = matching_agency_rows[0]
        else:
            print 'scalar not returned for ', row['agency_name'], ';', len(matching_agency_rows), 'results found instead'
            continue
        row['attachments_count'] = new_report_row['attachments_count']
        row['attachment_ids\n']
        new_report_row['attachment_ids\r\n']
        row['request_id'] = new_report_row['request_id']
        outcsv.writerow(row)

    outfile.close()


# TODO: tool to join messages with requests (for manual forwards from gmail ... look up thread id somewhere ... start from all attachments) - 1 hr

# TODO: report contacts of agencies that didn't submit (easy) - 0.5 hr

# TODO: auto-send to agencies that didn't submit (crib off old script) - 0.5 hr 

