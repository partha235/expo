import ubinascii
import urequests
import config
import network
import utime
from machine import Pin


x=Pin(14,Pin.IN,Pin.PULL_UP)  # connected pullup resistor internally
# pullup resistor -> resistor between 3v and gpio pin

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Wi-Fi...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            utime.sleep(1)
    print('Network config:', sta_if.ifconfig())

class TwilioSMS:
    base_url = 'https://api.twilio.com/2010-04-01'

    def __init__(self, account_sid, auth_token):
        self.twilio_account_sid = account_sid
        self.twilio_auth = ubinascii.b2a_base64('{sid}:{token}'.format(
            sid=account_sid, token=auth_token)).strip()

    def create(self, body, from_, to):
        data = 'Body={body}&From={from_}&To={to}'.format(
            body=body, from_=from_.replace('+', '%2B'),
            to=to.replace('+', '%2B'))
        r = urequests.post(
            '{base_url}/Accounts/{sid}/Messages.json'.format(
                base_url=self.base_url, sid=self.twilio_account_sid),
            data=data,
            headers={'Authorization': b'Basic ' + self.twilio_auth,
                     'Content-Type': 'application/x-www-form-urlencoded'})
        print('SMS sent with status code', r.status_code)
        print('Response: ', r.text)
        
connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
while True:
    print(x.value())
    if not x.value():
        print("saga")
        sms = TwilioSMS(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        sms.create(body='im in danger please help me', from_=config.TWILIO_FROM_NUMBER,
                to=config.NOTIFICATION_NUMBER)
        utime.sleep(1)
