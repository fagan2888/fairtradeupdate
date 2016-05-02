import sendgrid

client = sendgrid.SendGridClient("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")
message = sendgrid.Mail()

message.add_to("garycheng@berkeley.edu")
message.set_from("inbound@fairtradeupdate.bymail.in")
message.set_subject("Sending with SendGrid is Fun")
message.set_html("and easy to do anywhere, even with Python")

status, msg = client.send(message)
print(status, msg)
