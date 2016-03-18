from apps.agency.models import Agency
from apps.users.models import User
from apps.requests.models import Request
from apps.government.utils import get_defaults, get_or_create_us_govt
from apps.contacts.models import Contact

#sender_username = 'matthewlkiefer'
sender_username = 'payroll2016'

me = User.objects.filter(username=sender_username)[0]
req = Request.objects.get(id=1)

def create_request(agency_name):
    """
    returns unsaved!
    """
    
    language, ntn, govt = get_defaults()
    govt = get_or_create_us_govt(agency_name,'city')
    agency, created = Agency.objects.get_or_create(name=agency_name,government=govt)
    contact = Contact.objects.get_or_create(first_name='FOIA Officer', last_name=agency_name)
    # if a query returns, get contact out of response tuple
    if type(contact) == tuple:
        contact = contact[0]
    agency.save()

    request = Request.objects.create(
                                     author_id = me.id,
                                     government_id = govt.id,
                                     agency_id = agency.id,
                                     text = req.text,
                                     free_edit_body = req.free_edit_body,
                                     title = req.title
                                    )


    contact.agency_related_contacts.add(agency)
    request.contacts.add(contact)


    return request
