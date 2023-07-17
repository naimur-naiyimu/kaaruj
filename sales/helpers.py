from io import BytesIO
from tempfile import tempdir
import traceback
from urllib import response
import uu
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

def sendPdfEmail(subject, message,  from_mail, to_mail, filepath):
    try:
        # email = EmailMessage(subject, message,  from_mail, to_mail)
        # email.attach_file(filepath)
        # email.send()
        msg = EmailMultiAlternatives(subject, message, from_mail, to_mail)
        msg.attach('invoice.pdf', open(filepath, 'rb').read(), 'application/pdf')
        msg.send()
    except Exception as e:
        traceback.print_exc()
        import logging
        logger = logging.getLogger('django')
        logger.error(f'-----------Invoice Create Issue in send email------------------')
        logger.error(f'{str(e)}')


def save_pdf(params):
    try:
        template = get_template("invoice/index.html")

        # print("params",params)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
        # file_name = "changeItlater"
        file_name = uuid.uuid4()

        try:
            with open(str(settings.BASE_DIR)+f'/media/invoice_pdf/{file_name}.pdf', 'wb+') as output:
                pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
        except Exception as e:
            traceback.print_exc()
        if pdf.err:
            return "", False
        return f"{settings.BASE_DIR}/media/invoice_pdf/{file_name}.pdf", True
    except Exception as e:
        traceback.print_exc()
        import logging
        logger = logging.getLogger('django')
        logger.error(f'-----------Save pdf issue in create invoicel------------------')
        logger.error(f'{str(e)}')
        return "", False
