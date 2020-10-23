from sendgrid.helpers.mail import *
import sendgrid
SENDGRID_API = "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"
FROM_EMAIL = 'deepak.dhanjal12@gmail.com'
FROM_NAME = 'Pubg'




def sendEmail( to_email, email_content):
    try:
        connection = sendgrid.SendGridAPIClient(api_key=SENDGRID_API)
        mail = Mail()
        mail.from_email = Email(FROM_EMAIL, FROM_NAME)
        personalization = Personalization()
        personalization.add_to(Email(to_email))
        mail.add_personalization(personalization)
        mail.subject = "Pubg by Dhanjal"
        
        mail.add_content(Content("text/html", email_content))
        send_mail = connection.send(mail)
        print(send_mail)

    except:
        print('Errr')

def getemailcontent():
    filepath = 'room.html'
    filecnt = open(filepath, 'r')
    emailcontent = filecnt.read()
    
    room_id = '2365566'
    emailcontent = emailcontent.replace('{{roomid}}', room_id)
    # print(emailcontent)
    return emailcontent



to_email = 'gcrew.nvdeep@gmail.com'
email = getemailcontent()
# # print(email)
sendEmail(to_email, email)


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='deepak.dhanjal12@gmail.com',
#     to_emails=to_email,
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(SENDGRID_API)

#     print('Email Sent')
#     response = sg.send(message)
#     print(response.status_code)
#     # print(response.body)
#     # print(response.headers)
# except Exception as e:
#     print(e.message)



