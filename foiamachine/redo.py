"""
find all agencies
that didn't get a FOIA yet
and send them one now
"""


from sets import Set
from apps.mail.models import MailMessage
from apps.agency.models import Agency, Contact
from apps.requests.models import Request
from apps.users.models import User


# START CONFIG
#

req = Request.objects.get(id=1)
me = User.objects.filter(username='matthewlkiefer')[0]

#
# END CONFIG


# all_tos = every email domain that got a foia
all_tos = Set([])
for mm in MailMessage.objects.all():
    for to in mm.to.all():
        if len(to.content.split('@')) > 1:
            all_tos.add(to.content.split('@')[1])


# if this agency isn't in all_tos, queue em up for redo
unsent_agencies = []
for agency in Agency.objects.all():
    agency_messages = []
    for contact in agency.contacts.all():
        for email in contact.emails.all():
             if email.content.split('@')[1] in all_tos:
                 agency_messages.append(email)
    if not agency_messages:
        unsent_agencies.append(agency)


# redo the foias for agencies that weren't sent one
for agency in unsent_agencies:
    for contact in agency.contacts.all():
        if list(contact.emails.all()):
            request = Request.objects.create(
                        author_id = me.id,
                        government_id = agency.government_id,
                        agency_id = agency.id,
                        text = req.text,
                        free_edit_body = req.free_edit_body,
                        title = req.title
                        )
            request.contacts.add(contact)
            print request.__dict__
            #request.delete()
            request.save()
            request.send()


