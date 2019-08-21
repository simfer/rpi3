# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

textfile = "pippo.txt"

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
with open(textfile, 'rb') as fp:
    # Create a text/plain message
    msg = MIMEText(fp.read())

me = "simmaco.ferriero@gmail.com"
you = "simmaco.ferriero@sap.com"
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

import textwrap
import smtplib

mysubject = "send test from python"
mytext = "simmaco simmaco"


server = smtplib.SMTP('smtp.gmail.com',587)

server.starttls()

server.login('simmaco.ferriero@gmail.com','')

server.sendmail(me,you,msg)

server.quit()
