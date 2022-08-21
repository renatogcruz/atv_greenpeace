from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def send_mail(service_name):

    message = Mail(
        from_email='contact1@greenpeace.com',
        to_emails='contact2@greenpeace.com',
        subject=f'Serviço de atualização de notícias - {service_name}',
        html_content=f'<strong>Serviço de atualização de notícias da {service_name} apresentou falhas. Verificar!</strong>')

    api_key = os.environ.get('SENDGRID_API_KEY')

    sg = SendGridAPIClient(api_key)

    response = sg.send(message)

    print(response.status_code, response.body, response.headers)

    r = 'success' if response.status_code == 202 else 'failed'

    return r
