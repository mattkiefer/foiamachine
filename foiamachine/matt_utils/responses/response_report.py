from sets import Set
from pprint import pprint
from apps.requests.models import *
from apps.contacts.models import *
from apps.mail.models import *
from cleanup import *

# TODO: get atts with *no* requests and fix those using email body/sender


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
    print 'assigning att.id', att.id, 'to request for', agency.name


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
                    attachments.append(att.file.name.encode())
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
    


# TODO: tool to join messages with requests (for manual forwards from gmail ... look up thread id somewhere ... start from all attachments) - 1 hr

# TODO: report contacts of agencies that didn't submit (easy) - 0.5 hr

# TODO: auto-send to agencies that didn't submit (crib off old script) - 0.5 hr 

