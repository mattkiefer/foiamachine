# IPython log file

import csv 
from apps.government.utils import get_defaults, get_or_create_us_govt
from apps.agency.models import Agency
from apps.contacts.models import Contact
from apps.contacts.models import EmailAddress
from apps.users.models import User
from apps.requests.models import Request
from django.conf import settings
me = User.objects.get(username='matthewlkiefer')
language, ntn, govt = get_defaults()
govt = get_or_create_us_govt('All Elementary/High School Employees','city')
agency, created = Agency.objects.get_or_create(name='All Elementary/High School Employees',government=govt)
contact, created = Contact.objects.get_or_create(first_name='FOIA', middle_name='', last_name='Officer')
contact.add_email('NA')
agency.contacts.add(contact)
agency.creator_id = me.id
contact.save()
agency.save()


req = Request.objects.get(id=1)
request = Request.objects.create(
                           author_id= me.id,
                            government_id = govt.id,
                            agency_id = agency.id,
                            text = req.text,
                            free_edit_body = req.free_edit_body,
                            title = req.title)
request.contacts.add(contact)
request.save()
from matt_utils.responses.response_report import relate_att_to_agency
get_ipython().magic(u'pinfo2 relate_att_to_agency')
get_ipython().magic(u'pinfo relate_att_to_agency')
from apps.requests.models import Attachment
get_ipython().magic(u'pinfo relate_att_to_agency')
agency
agency.save()
agency.id
relate_att_to_agency(Attachment.objects.get(id=855),agency.id)
get_ipython().magic(u'logstart all_school_emp.log')
get_ipython().magic(u'ls ')
agency
agency.id
Attachment.objects.get(id=855)
Attachment.objects.get(id=855).file.name
isbe_csv = Attachment.objects.get(id=855)
