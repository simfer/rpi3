import email
import smtplib

msg = email.message_from_string('warning')
msg['From'] = "simmaco.ferriero@live.it"
msg['To'] = "simmaco.ferriero@gmail.com"
msg['Subject'] = "Ciao a tutti"

s = smtplib.SMTP("smtp.live.com",587)
s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
s.starttls() #Puts connection to SMTP server in TLS mode
s.ehlo()
s.login('simmaco.ferriero@live.it', 'frr68smc')

s.sendmail("simmaco.ferriero@live.it", "simmaco.ferriero@gmail.com", msg.as_string())

s.quit()