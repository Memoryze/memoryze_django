from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data['email_subject'], body=data['html_content'], to=[data['to_email']])
        email.content_subtype = 'html'
        email.send()
