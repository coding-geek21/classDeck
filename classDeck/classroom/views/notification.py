from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from django.conf import settings
from ..models import Assignment, Student

def send_notification(assignment):
    students = Student.objects.all()
    url = f'classdeck.herokuapp.com/students/response/add/{assignment.id}'
    for i in students:
        print(i)
        print(i.interests.all)
        if assignment.subject in i.interests.all():
            print("found")
            send_mail(assignment, i.user.username, i.user.email, url)
    return 0

def send_mail(assignment, username, email, url):
    message = get_template("email_notification/assignment_notify_mail.html").render({
        'assignment': assignment,
        'student': username,
        'url': url
    })
    mail = EmailMessage(
        subject= f"New ASSIGNMENT ({assignment.subject.name}) from classDeck",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    return mail.send()