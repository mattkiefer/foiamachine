from apps.agency.models import Agency
from apps.users.models import User
from apps.requests.models import Request
from apps.government.utils import get_defaults, get_or_create_us_govt


sender_username = 'matthewlkiefer'

me = User.objects.filter(username=sender_username)[0]
req = Request.objects.get(id=1)

def create_request(agency):
    """
    returns unsaved!
    """
    
    language, ntn, govt = get_defaults()
    govt = get_or_create_us_govt(agency.name,'city')
    agency, created = Agency.objects.get_or_create(name=agency.name,government=govt)
    agency.save()

    request = Request.objects.create(
                                     author_id = me.id,
                                     government_id = govt.id,
                                     agency_id = agency.id,
                                     text = req.text,
                                     free_edit_body = req.free_edit_body,
                                     title = req.title
                                    )
    
    for contact in agency.contacts.all():
        request.contacts.add(contact)

    return request
