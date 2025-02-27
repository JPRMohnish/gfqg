from email.message import Message
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from flask.helpers import send_file


def send_email(TO, Body, Subject):
    FROM = sys.argv[1]
    PassWord = sys.argv[2]

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = Subject
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM  # email pass are passed from cli
    MESSAGE.preamble = """ Try Solving these problems again. Happy Learning! """

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(Body, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)
    print("Sending")
    # The actual sending of the e-mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(FROM, PassWord)
        server.sendmail(
            FROM, TO, MESSAGE.as_string()
        )
        server.quit()
    print("Sent successfully")
    return "email sent successfully"


class RevisionEmails:
    def __init__(self, schedule):
        self.schedule = schedule
        pass

    def format_html(self, content):
        data = "<ol>"
        for dat in content:
            print(dat)
            data = data + \
                f'<li>{dat["question"]} <br> <ul> <li>wrong:-- {dat["wrong_answer"]} </li><li>correct:-- {dat["correct_answer"]} </li></ul></li>'
        data = data + "</ol>"
        return data

    def schedule_email(self, plan, data, TO, Subject):
        data = self.format_html(data)
        if plan['day'] == 'monday':
            self.schedule.every().monday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'tuesday':
            self.schedule.every().tuesday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'wednesday':
            self.schedule.every().wednesday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'thursday':
            self.schedule.every().thursday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'friday':
            self.schedule.every().friday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'saturday':
            self.schedule.every().saturday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        elif plan['day'] == 'sunday':
            self.schedule.every().sunday.at(plan['time']).do(
                send_email, TO=TO, Body=data, Subject=Subject)
        return 'email scheduled successfully'
        # bug here we need to make this code asynchronous in python.
