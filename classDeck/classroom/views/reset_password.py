from classDeck.settings import DEBUG
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordResetForm
from classroom.models import User
from django.contrib.auth.forms import SetPasswordForm


class AbstractUserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        self.user = User
        super().__init__(*args, **kwargs)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(subject_template_name, context)
        context["domain"] = context["site_name"] = "classdeck.herokuapp.com"
        if DEBUG:
            context["domain"] = context["site_name"] = "localhost:8000"
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-Mail address."
            self.add_error('email', msg)
        return email


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'reset_password/password_reset.html'
    email_template_name = 'reset_password/password_reset_email.html'
    form_class = EmailValidationOnForgotPassword
    subject_template_name = 'reset_password/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "You should receive them shortly." \
                      " If you don't receive an email, " \
                      "kindly check your spam folder."
    success_url = reverse_lazy('home')

