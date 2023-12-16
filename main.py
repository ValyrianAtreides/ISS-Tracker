import requests
from datetime import datetime
import  smtplib
import time

MY_LAT = 37.860920 # Your latitude
MY_LONG = 27.257339 # Your longitude
user="mail@gmail.com" #Your e-mail
password="password" #Your Password
to_addres="merha@merhaba.com" #Which e-mail to send
def is_iss_close():
    if abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5:
        return True
    return False
def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=user, password=password)
        connection.sendmail(from_addr=user,
                            to_addrs=to_addres,
                            msg=f"Subject:Look Up ISS is in the air\n\nISS is in the air at your locaiton")

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
while True:
    time.sleep(60)
    if is_iss_close() and time_now.hour < sunset:
        send_email()