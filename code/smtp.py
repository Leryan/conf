#!/usr/bin/env python2

import smtplib
import email.utils
import time
import random
import email
from email.mime.text import MIMEText
import base64

options = {
    'spam': False,
    'novirus': False
}
dest='dest@peterschmitt.fr'
author = 'test@peterschmitt.fr'

text = """
Subject: Test spam mail (GTUBE)
Message-ID: <GTUBE1.1010101@example.net>
Date: Wed, 23 Jul 2003 23:30:00 +0200
From: Sender <sender@example.net>
To: Recipient <recipient@example.net>
Precedence: junk
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

This is the GTUBE, the
	Generic
	Test for
	Unsolicited
	Bulk
	Email

If your spam filter supports it, the GTUBE provides a test by which you
can verify that the filter is installed correctly and is detecting incoming
spam. You can send yourself a test mail containing the following string of
characters (in upper case and with no white spaces and line breaks):


You should send this test mail from an account outside of your network.
"""

#text = 'Message de test.'

text += str(time.time() + random.random())

# Create the message
#msg = MIMEText(text)
html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
html +='"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
html +='<body style="font-size:12px;font-family:Verdana"><p>This is a test message.<p>'
if options['spam']:
    html += text
html += "</body></html>"
msg = email.MIMEMultipart.MIMEMultipart('alternative')
msg.attach(email.mime.text.MIMEText(html,'html'))

fileMsg = email.mime.base.MIMEBase('application','pdf')
if options['novirus']:
    fileMsg.set_payload(base64.b64decode("JVBERi0xLjEKJdDQ0NAKCjEgMCBvYmoKPDwKIC9UeXBlIC9DYXRhbG9nCiAvT3V0bGluZXMgMiAwIFIKIC9QYWdlcyAzIDAgUgogL05hbWVzIDw8IC9FbWJlZGRlZEZpbGVzIDw8IC9OYW1lcyBbKC9kZXYvbnVsbCkgNyAwIFJdID4+ID4+Cj4+CmVuZG9iagoKMiAwIG9iago8PAogL1R5cGUgL091dGxpbmVzCiAvQ291bnQgMAo+PgplbmRvYmoKCjMgMCBvYmoKPDwKIC9UeXBlIC9QYWdlcwogL0tpZHMgWzQgMCBSXQogL0NvdW50IDEKPj4KZW5kb2JqCgo0IDAgb2JqCjw8CiAvVHlwZSAvUGFnZQogL1BhcmVudCAzIDAgUgogL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KIC9Db250ZW50cyA1IDAgUgogL1Jlc291cmNlcyA8PAogICAgICAgICAgICAgL1Byb2NTZXQgWy9QREYgL1RleHRdCiAgICAgICAgICAgICAvRm9udCA8PCAvRjEgNiAwIFIgPj4KICAgICAgICAgICAgPj4KPj4KZW5kb2JqCgo1IDAgb2JqCjw8IC9MZW5ndGggNDUgPj4Kc3RyZWFtCkJUIC9GMSAxMiBUZiA3MCA3MDAgVGQgMTUgVEwgKFlheSBQREZzKSBUaiBFVAplbmRzdHJlYW0KZW5kb2JqCgo2IDAgb2JqCjw8CiAvVHlwZSAvRm9udAogL1N1YnR5cGUgL1R5cGUxCiAvTmFtZSAvRjEKIC9CYXNlRm9udCAvSGVsdmV0aWNhCiAvRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCgo3IDAgb2JqCjw8CiAvVHlwZSAvRmlsZXNwZWMKIC9GICgvZGV2L251bGwpCiAvRUYgPDwgL0YgOCAwIFIgPj4KPj4KZW5kb2JqCgo4IDAgb2JqCjw8CiAvTGVuZ3RoIDgKIC9GaWx0ZXIgL0ZsYXRlRGVjb2RlCiAvVHlwZSAvRW1iZWRkZWRGaWxlCj4+CnN0cmVhbQp4nAMAAAAAAQplbmRzdHJlYW0KZW5kb2JqCgp4cmVmCjAgOQowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTYgMDAwMDAgbiAKMDAwMDAwMDE0NyAwMDAwMCBuIAowMDAwMDAwMTk2IDAwMDAwIG4gCjAwMDAwMDAyNTcgMDAwMDAgbiAKMDAwMDAwMDQ0OSAwMDAwMCBuIAowMDAwMDAwNTQ1IDAwMDAwIG4gCjAwMDAwMDA2NTkgMDAwMDAgbiAKMDAwMDAwMDczNCAwMDAwMCBuIAp0cmFpbGVyCjw8CiAvU2l6ZSA5CiAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKODM2CiUlRU9GCg=="))
    fileMsg.add_header('Content-Disposition','attachment;filename=harmless-test-file.pdf')
else:
    fileMsg.set_payload(base64.b64decode("JVBERi0xLjEKJdDQ0NAKCjEgMCBvYmoKPDwKIC9UeXBlIC9DYXRhbG9nCiAvT3V0bGluZXMgMiAwIFIKIC9QYWdlcyAzIDAgUgogL05hbWVzIDw8IC9FbWJlZGRlZEZpbGVzIDw8IC9OYW1lcyBbKEVJQ0FSKSA3IDAgUl0gPj4gPj4KPj4KZW5kb2JqCgoyIDAgb2JqCjw8CiAvVHlwZSAvT3V0bGluZXMKIC9Db3VudCAwCj4+CmVuZG9iagoKMyAwIG9iago8PAogL1R5cGUgL1BhZ2VzCiAvS2lkcyBbNCAwIFJdCiAvQ291bnQgMQo+PgplbmRvYmoKCjQgMCBvYmoKPDwKIC9UeXBlIC9QYWdlCiAvUGFyZW50IDMgMCBSCiAvTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQogL0NvbnRlbnRzIDUgMCBSCiAvUmVzb3VyY2VzIDw8CiAgICAgICAgICAgICAvUHJvY1NldCBbL1BERiAvVGV4dF0KICAgICAgICAgICAgIC9Gb250IDw8IC9GMSA2IDAgUiA+PgogICAgICAgICAgICA+Pgo+PgplbmRvYmoKCjUgMCBvYmoKPDwgL0xlbmd0aCA0NSA+PgpzdHJlYW0KQlQgL0YxIDEyIFRmIDcwIDcwMCBUZCAxNSBUTCAoWWF5IFBERnMgWDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCopIFRqIEVUCmVuZHN0cmVhbQplbmRvYmoKCjYgMCBvYmoKPDwKIC9UeXBlIC9Gb250CiAvU3VidHlwZSAvVHlwZTEKIC9OYW1lIC9GMQogL0Jhc2VGb250IC9IZWx2ZXRpY2EKIC9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKCjcgMCBvYmoKPDwKIC9UeXBlIC9GaWxlc3BlYwogL0YgKEVJQ0FSKQogL0VGIDw8IC9GIDggMCBSID4+Cj4+CmVuZG9iagoKOCAwIG9iago8PAogL0xlbmd0aCA3NwogL0ZpbHRlciAvRmxhdGVEZWNvZGUKIC9UeXBlIC9FbWJlZGRlZEZpbGUKPj4Kc3RyZWFtCnicizD1VwxQdXAMiDaJCYiKMDXRCIjTNHd21jSvVXH1dHYM0g0OcfRzcQxy0XX0C/EM8wwKDdYNcQ0O0XXz9HFVVPHQ9tDiAgCGbRIZCmVuZHN0cmVhbQplbmRvYmoKCnhyZWYKMCA5CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNiAwMDAwMCBuIAowMDAwMDAwMTQzIDAwMDAwIG4gCjAwMDAwMDAxOTIgMDAwMDAgbiAKMDAwMDAwMDI1MyAwMDAwMCBuIAowMDAwMDAwNDQ1IDAwMDAwIG4gCjAwMDAwMDA1NDEgMDAwMDAgbiAKMDAwMDAwMDY1NSAwMDAwMCBuIAowMDAwMDAwNzI2IDAwMDAwIG4gCnRyYWlsZXIKPDwKIC9TaXplIDkKIC9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgo4OTgKJSVFT0YK"))
    fileMsg.add_header('Content-Disposition','attachment;filename=eicar-test-file.pdf')
email.encoders.encode_base64(fileMsg)
msg.attach(fileMsg)

msg['To'] = email.utils.formataddr(('Recipient', dest))
msg['From'] = email.utils.formataddr(('Author', author))
msg['Subject'] = 'test viraloupa'

server = smtplib.SMTP('smtp.peterschmitt.fr')
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail(author, [dest,], msg.as_string())
finally:
    server.quit()
