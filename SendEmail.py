import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailWithAtachment:
    def __init__(self, email):

        self.from_address = email['from_address']
        self.to_address = email['to_address']
        self.subject = email['subject']
        self.message_body = email['message_body']
        self.file_to_send = email['file_to_send']
        self.smtp_server = email['smtp_server']
        self.server_credentials = email['server_credentials']


    def build_message(self):

        message_to_send = MIMEMultipart()
        message_to_send['From'] = self.from_address
        message_to_send['To'] = self.to_address
        message_to_send['Subject'] = self.subject

        message_to_send.attach(MIMEText(self.message_body,'plain'))

        open_file_to_attach = open(self.file_to_send, 'rb')
        message_part = MIMEBase('application', 'octet-stream')
        message_part.set_payload((open_file_to_attach).read())
        encoders.encode_base64(message_part)
        message_part.add_header('Content-Disposition', 'attachment; filename= %s' % self.file_to_send)

        message_to_send.attach(message_part)

        open_file_to_attach.close()

        return message_to_send

    def send_the_message(self, message_to_send):

        try:
            email_server = smtplib.SMTP_SSL(self.smtp_server['server_address'], self.smtp_server['server_port'])
            email_server.ehlo()

            email_server.login(self.server_credentials['login'], self.server_credentials['password'])

            message = message_to_send.as_string()
            email_server.sendmail(self.from_address, self.to_address, message)
            email_server.quit()
            print("The email was sent!")

        except smtplib.SMTPResponseException as e:
            error_code = e.smtp_code
            error_message = e.smtp_error
            print(f"Can't send the email or connect to email server!\n"
                  f" error code = {error_code}\n"
                  f" error message = {error_message}")
