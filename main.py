import requests, time, smtplib
from datetime import datetime

MY_LAT = "YOUR LATITUDE"
MY_LONG = "YOUR LONGITUDE"
my_email = "YOUR-EMAIL"
password = "YOUR-PASSWORD"
email_receiver = "RECEIVER-EMAIL"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if iss_latitude in range(int(MY_LAT-5), int(MY_LAT+6)) and iss_longitude in range(int(MY_LONG-5),int(MY_LONG+6)):
        return True

def is_night():
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
    time_now = datetime.now().hour
    if time_now in range(sunrise, sunset+1):
        return True

while is_iss_overhead() and is_night():
    time.sleep(60)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email_receiver,
            msg="Subject:ISSO overhead!\n\nThe ISS is above you in the sky."
        )
