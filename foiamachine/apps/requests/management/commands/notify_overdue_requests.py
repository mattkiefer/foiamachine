from apps.requests.models import Request, Notification
import json
import logging
import requests
import settings
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        nargs = len(args)
        if nargs == 0:
            ndays = -1
        elif nargs > 1:
            raise CommandError("Usage: notify_overdue_requests [ndays]")
        elif nargs == 1:
            try:
                ndays = int(args[0])
            except ValueError:
                raise CommandError("%s not an integer number of days" % args[0])

        therequests = Request.get_all_overdue()

        for request in therequests:
            print 'Doing request %s response due %s' % (request.id, request.get_due_date)

            user = request.author
            address = user.email
            try:
                address = settings.TASK_EMAIL_RECIPIENT
            except:
                pass
            notifcation = Notification(type=Notification.get_type_id("Late request"), request=request)
            notifcation.save()

            data = {
                "from" : "admin@foiamachine.org",
                "to" : address,
                'subject' : 'Response due from ' + request.agency.name,
                'html' : """
                    According to our records, you're overdue to receive a response from %s. <br />
                    If that's not the case, you can log in and update the status of your request
                    at <a href="https://www.foiamachine.org/requests/%s">https://www.foiamachine.org/requests/%s</a>
                    """ % (request.agency.name, request.pk, request.pk)
            }

            if settings.MG_ROUTE:
                post_url = 'https://api.mailgun.net/v2/%s.%s/messages' % (settings.MG_ROUTE, settings.MG_DOMAIN)
            else:
                post_url = 'https://api.mailgun.net/v2/%s/messages' % settings.MG_DOMAIN

            if settings.SEND_NOTIFICATIONS:
                resp = requests.post(
                        post_url,
                        auth=("api", settings.MAILGUN_KEY),
                        data=data)
                content = json.loads(resp.content)
                logging.info('SENT NOTIFICATION STATUS:%s' % content)
