from twilio.rest import Client

def send_twilio_sms(message):
    account_sid = 'ACe3f8717a9a56fa1ee6a095fc86a369ce'
    auth_token = '3f512d18ea38a6294ec7fefe11072eed'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+19497102331',
        body="REAL-TIME UPDATE: "+message,
        to='+918104982720'
    )

    print(f"SMS sent with SID: {message.sid}")

if __name__ == '__main__':
    send_twilio_sms()
