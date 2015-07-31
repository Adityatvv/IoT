from twilio.rest import TwilioRestClient 
 
def mes(text):
    # put your own credentials here 
    ACCOUNT_SID = "AC871104bc88d5c967459ddbe9d11cbb4d" 
    AUTH_TOKEN = "37eead14fa6fe0118300d43e934d2879" 
 
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
    client.messages.create(
        	to="3306223162", 
	        from_="+13307524648", 
	        body=str(text),  
    )
    print "Message Sent"
