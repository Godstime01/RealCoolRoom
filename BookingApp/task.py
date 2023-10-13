from celery import shared_task
from .models import BookingModel


from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"

@shared_task(bind=True)
def send_expiration_mail(self):
    now = timezone.now()
    due_bookings = BookingModel.objects.filter(due_date__lte=now)

    for booking in due_bookings:
        subject = 'BookingModel Reminder'
        message = f'Your booking on {booking.due_date} is due soon.'
        recipient_list = [booking.user.email]

        # Load and render the email template
        email_template = 'BookingApp/notification_email.html'
        context = {'subject': subject, 'message': message}
        email_content = render_to_string(email_template, context)

        # Create an EmailMessage instance
        email = EmailMessage(subject, email_content, 'your-email@example.com', recipient_list)
        email.content_subtype = 'html'

        # Send the email
        email.send()