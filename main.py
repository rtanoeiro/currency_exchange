from utils.email_api import Email
from utils.email_addresses import EMAILS

email = Email()
email.send_email_without_attachment(receiver=[EMAILS["RAMON_EMAIL"], EMAILS["REGINA_EMAIL"]], subject="Test email")
