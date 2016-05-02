import sys
import imaplib
import getpass
import email
import email.header
import datetime
import smtplib
from flask import Flask, request
import simplejson
import sendgrid
import re
import requests
app = Flask(__name__)


EMAIL_ACCOUNT = "fairtradeupdate@gmail.com"
PASSWORD = "berkeleybuilds"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "INBOX"
ERRORS = [0]

EMAIL_BODY = "Welcome to Fair Trade Update. This purpose of this email is to find out: Q1. How much and what was the premium was spent for Q2. An estimate of how many people the premium helped. Please preface your response to each question with 'START_Q#' and end your response with 'END_Q#'"

EMAIL_SUBJ = "FAIR TRADE UPDATE: "
SENDING = True

# @app.route('/inmail', methods=['POST'])
# def f():
#
#     return "OK"


def send_email(destination, subject, text):
    client = sendgrid.SendGridClient("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")
    message = sendgrid.Mail()

    message.add_to(destination)
    message.set_from("inbound@fairtradeupdate.bymail.in")
    message.set_subject(subject)
    message.set_html(text)

    status, msg = client.send(message)
    print(status, msg)

def send_updates():
    if SENDING == True:
        projects = requests.get('http://localhost:5001/projects').json()["projects"]
        for project in projects:
            dest_email = project.project_email
            subject = EMAIL_SUBJ
            project_id = project.project_id
            send_email(dest_email, subject + "IDENTIFICATION:" + project_id, EMAIL_BODY)



@app.route('/inmail', methods=['POST'])
def sendgrid_parser():
  # Consume the entire email
  envelope = simplejson.loads(request.form.get('envelope'))

  # Get some header information
  to_address = envelope['to'][0]
  from_address = envelope['from']

  # Now, onto the body
  text = request.form.get('text')
  html = request.form.get('html')
  subject = request.form.get('subject')

  #print(text)

  # proj_id = "DEFAULT"
  # answer1 = "DEFAULT"
  # answer2 = "DEFAULT"

  proj_id = re.findall(r'IDENTIFICATION:(?s)(.*)', subject)
  if proj_id:
    print(proj_id[0])

  answer3 = re.findall(r'START_Q3(?s)(.*)END_Q3', text)
  if answer3:
      print(answer3[0])

  answer1 = re.findall(r'START_Q1(?s)(.*)END_Q1', text)
  if answer1:
      print(answer1[0])

  answer2 = re.findall(r'START_Q2(?s)(.*)END_Q2', text)
  if answer2:
      print(answer2[0])

  status = requests.get('http://localhost:5001/update?money='+str(answer1[0])+"&people="+str(answer2[0])+"&description="+str(answer3[0])+"&project_id="+str(proj_id[0])).json()["status"]

  if status == "success":
      return "OK"
  else:
      return "NOT OK"

#PRINT FUNCTION
def adv_print(s):
    print("$$$$$$$$$$$$$$$$")
    print(str(s) + "; " + str(ITER))
    ITER[0] = ITER[0] + 1
    print("$$$$$$$$$$$$$$$$")

if __name__ == '__main__':
    #send_email("garycheng@berkeley.edu", EMAIL_SUBJ, EMAIL_BODY)
    #send_updates()
    app.run(debug=True)
