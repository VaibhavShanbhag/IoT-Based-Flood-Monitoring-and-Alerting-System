import conf
from boltiot import Sms, Email, Bolt
import json, time

intermediate_value = 55
max_value = 80


mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECIPIENT_EMAIL)


def twillo_message(message):
  try:
     print("Making request to Twilio to send a SMS")
     response = sms.send_sms(message)
     print("Response received from Twilio is: " + str(response))
     print("Status of SMS at Twilio is :" + str(response.status))
  except Exception as e:
     print("Below are the details")
     print(e)

def mailgun_message(head,message_1):
  try:
     print("Making request to Mailgun to send an email")
     response = mailer.send_email(head,message_1)
     print("Response received from Mailgun is: " + response.text)
  except Exception as e:
     print("Below are the details")
     print(e)
     
while True:
    print ("Reading Water-Level Value")
    response_1 = mybolt.serialRead('10')
    response = mybolt.analogRead('A0')
    data_1 = json.loads(response_1)
    data = json.loads(response) 
    Water_level = data_1['value'].rstrip()
    print("Water Level value is: " + str(Water_level) + "%")
    sensor_value = int(data['value'])
    temp = (100*sensor_value)/1024
    temp_value = round(temp,2)
    print("Temperature is: " + str(temp_value) + "°C")
    try: 
 
        if int(Water_level) >= intermediate_value:
            message ="Orange Alert!. Water level is increased by " +str(Water_level) + "% at your place. Please be Safe. The current Temperature is " + str(temp_value) + "°C."
            head="Orange Alert"
            message_1="Water level is increased by " + str(Water_level) + "% at your place. Please be Safe. The current Temperature is " + str(temp_value) + "°C."
            twillo_message(message)
            mailgun_message(head,message_1)

        if int(Water_level) >= max_value:
           message ="Red Alert!. Water level is increased by " + str(Water_level) + "% at your place. Please Don't move out of the house. The Current Temperature is " + str(temp_value) + "°C"
           head="Red Alert!"
           message_1="Water level is increased by " + str(Water_level) + "% at your place. Please Don't move out of the house. The Current Temperature is " + str(temp_value) + "°C."
           twillo_message(message)
           mailgun_message(head,message_1)

    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(15)
