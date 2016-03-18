import csv
from apps.government.utils import get_defaults, get_or_create_us_govt
from apps.agency.models import Agency
from apps.contacts.models import Contact
from apps.contacts.models import EmailAddress
from apps.users.models import User
from apps.requests.models import Request
from django.conf import settings

"""
******************************************
*** REMEMBER TO TURN OFF DJANGO DEBUG! ***
******************************************
"""

###############
# START CONFIG

sender_username = 'payroll2016' # TODO: abstract this
infilename = '/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/contacts/contacts_2016.csv'
#req = Request.objects.get(id=1) # request template to clone varies for IL, IN, WI, MO
req_text = open('/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/contacts/request.txt').read()
req_free = open('/home/ubuntu/foiamachine/repo/foiamachine/matt_utils/contacts/request_free.txt').read() # hack
req_title = 'Payroll FOIA'
error_log = open('error.log','w')
test = False
send = False
#TODO: figure out tags
 
# END CONFIG
##############

infile = open(infilename,'r')
incsv = csv.DictReader(infile)
error_csv = csv.writer(error_log)
icontacts = []
for irow in incsv:
    orow = {
            'government': irow['government'],
            'first_name': irow['first_name'],
            'last_name': irow['last_name'],
            'title': irow['title'],
            'phone': irow['phone'],
           }
    # for testing, override the email with this test recipient
    if test:
        orow['email'] = 'bga.payroll.2016+' + irow['government'].replace(' ','') + '@gmail.com'
    else:
        orow['email'] = irow['email']

    # easy way to skip all the empty rows
    if '@' not in orow['email']:
        continue
    # name the nameless
    if not orow['first_name'] and not orow['last_name']:
        orow['first_name'] = 'FOIA Officer'
        orow['last_name'] = orow['government']
    icontacts.append(orow)
    print orow

# sender
me = User.objects.filter(username=sender_username)[0]

for icontact in icontacts:
    # don't spam ... need to map this to current request in future cases (tags?)
    if list(EmailAddress.objects.filter(content=icontact['email'])) and not test:
        # print 'contact exists:', icontact['email']
        pass #continue

    try:
        language, ntn, govt = get_defaults()
        govt = get_or_create_us_govt(icontact['government'],'city') # TODO fix dumb hardcoded gov type using string inferences
        agency, created = Agency.objects.get_or_create(name=icontact['government'],government=govt)
        # TODO: NEED TO USE EMAIL FOR GET OR CREATE
        contact, created = Contact.objects.get_or_create(first_name=icontact['first_name'], middle_name='', last_name=icontact['last_name'])
        contact.add_email(icontact['email'])
        agency.contacts.add(contact)
        agency.creator_id = me.id
        contact.save()
        agency.save()
    
        # create request for each contact
        request = Request.objects.create(
                            author_id= me.id, 
                            government_id = govt.id, 
                            agency_id = agency.id, 
                            text = req_text, 
                            free_edit_body = req_free, 
                            title = req_title + ' | ' + agency.name
                           )
        request.contacts.add(contact)
        request.save()
        # adding custom lookup
        request.text = request.text + '\n\n' + request.thread_lookup
        request.free_edit_body = request.free_edit_body + '\n\n' + request.thread_lookup
        request.save()
        if send:
            request.send()
    except Exception, e:
        error_csv.writerow([icontact['email'],e])

error_log.close() 
