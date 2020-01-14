import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.main.config import Config

def _send_mail(to, data, template_id, html_content=''):
    message = Mail(
        from_email='GoToken <noreply@gotoken.io>',
        to_emails=to,
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    
    message.dynamic_template_data = data
    message.template_id = template_id

    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def send_reset_pwd_mail(to,token):
    data = {
        'reset_link': Config.GT_DOMAIN + '/reset-password/' + token,
    }
    template_id = 'd-da7bf0be41f24145a75b64e338972044'
    _send_mail(to=to, data=data, template_id=template_id)


