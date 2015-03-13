import csv
from apps.government.utils import get_defaults, get_or_create_us_govt
from apps.agency.models import Agency
from apps.contacts.models import Contact
from apps.contacts.models import EmailAddress
from apps.users.models import User
from apps.requests.models import Request
from django.conf import settings

# REMEMBER TO TURN OFF DEBUG!

###############
# START CONFIG

sender_username = 'matthewlkiefer'
infilename = 'contacts.csv'
req = Request.objects.get(id=668) # request template to clone 1:IL, 650:IN, 657:WI, 668:MO
error_log = open('error.log','w')
test = True
#TODO: figure out tags
 
# END CONFIG
##############

if test:
   infilename = 'test.csv'

infile = open(infilename,'r')
incsv = csv.reader(infile)
error_csv = csv.writer(error_log)
icontacts = []
for irow in incsv:
    orow = {
            'government': irow[1],
            'first_name': irow[3],
            'last_name': irow[4],
            'title': irow[5],
            'email': irow[6],
            'phone': irow[7],
           }

    # easy way to skip all the empty rows
    if '@' not in orow['email']:
        continue
    # name the nameless
    if not orow['first_name'] and not orow['last_name']:
        orow['first_name'] = 'FOIA Officer'
        orow['last_name'] = orow['government']
    icontacts.append(orow)

# sender
me = User.objects.filter(username=sender_username)[0]

for icontact in icontacts:
    # don't spam ... need to map this to current request in future cases (tags?)
    if list(EmailAddress.objects.filter(content=icontact['email'])) and not test:
        continue
    try:
        language, ntn, govt = get_defaults()
        govt = get_or_create_us_govt(icontact['government'],'city') # TODO fix dumb hardcoded gov type using string inferences
        agency, created = Agency.objects.get_or_create(name=icontact['government'],government=govt)
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
                            text = req.text, 
                            free_edit_body = req.free_edit_body, 
                            title = req.title
                           )
        request.contacts.add(contact)
        request.save()
        request.send()
    except Exception, e:
        error_csv.writerow(icontact.append(e))

error_log.close() 
