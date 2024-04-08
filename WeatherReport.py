#WeatherReport.py
#
# Kevin McEntee
# 4/1/2024
# Send Weather forecast via messaging service.

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# import required modules
import smtplib
from email.message import EmailMessage
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

# Get the raw data from the OpenWeather website and pull out the individual weather attributes.

weatherData = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q=bohemia,ny,us&appid=75a77152b4364c4b56380f7e4fcfe4c7&units=imperial")

weatherDataJson = weatherData.json()

allparagraphs = []

for items in weatherDataJson["list"]:

    weatherTime = items['dt']
    formattedWeatherTime = datetime.datetime.fromtimestamp(weatherTime).strftime('%Y-%m-%d %H:%M:%S')
    weatherPrediction = items['weather'][0]['main']
    weatherTemp = str(round(items['main']['temp']))
    weatherFeelsLike = str(round(items['main']['feels_like']))
    weatherTempMin = str(round(items['main']['temp_min']))
    weatherTempMax = str(round(items['main']['temp_max']))
    weatherHumidity = str(round(items['main']['humidity']))
    weatherClouds = items['clouds']['all']
    weatherWindSpeed = items['wind']['speed']

    # Start off the inclement weather notifications with empty strings and then populate them if necessary.

    msgSnowPrediction = ("")
    msgColdPrediction = ("")
    msgHeatPrediction = ("")
    msgRainPrediction = ("")

    if weatherPrediction == "Snow":
        msgSnowPrediction = ("Massive Snow!")

    if int(weatherTemp) <= 32:
        msgColdPrediction = ("Winter Cold!")

    if int(weatherTemp) >=  90:
        msgHeatPrediction = ("Summer Heat!")

    if weatherPrediction == "Rain":
        msgRainPrmediction = ("Massive Rain!")

    msgTime = ("Time: " + formattedWeatherTime + "\n")
    msgPrediction = ("Predicted Weather: " + weatherPrediction + "\n")
    msgTemperature = ("Predicted Temperature " + weatherTemp + "\n")
    msgFeelsLike = ("Predicted Feels Like: " + weatherFeelsLike + "\n")
    msgTempMin = ("Predicted Minimum Temperature: " + weatherTempMin + "\n")
    msgTempMax = ("Predicted Maximum Temperature: " + weatherTempMax + "\n") 
    msgHumidity = ("Predicted Humidity: " + weatherHumidity + "\n")
    msgClouds = ("Predicted Cloudiness in Percent: " + str(weatherClouds) + "\n")
    msgWindSpeed = ("Predicted Wind Speed: " + str(weatherWindSpeed) + "\n")

    if weatherPrediction == "Snow":
        msgSnowPrediction = ("Massive Snow!\n")

    if int(weatherTemp) <= 32:
        msgColdPrediction = ("Winter Cold!!\n")

    if int(weatherTemp) >=  90:
        msgHeatPrediction = ("Summer Heat!\n")

    if weatherPrediction == "Rain":
        msgRainPrediction = ("Massive Rain!\n")

    weatherMsg = "Weather Forecast Bohemia, NY:\n" + msgTime + msgPrediction + msgTemperature + msgFeelsLike + msgTempMin + msgTempMax + msgHumidity + msgClouds + msgWindSpeed + msgSnowPrediction + msgColdPrediction + msgHeatPrediction + msgRainPrediction
    allparagraphs.append(weatherMsg)
    print(weatherMsg)
    print("*********************************")

# Email account credentials

receiver_email = input("Enter your email address (e.g., yourname@example.com): ")
sender_email = "kjmcenteeusa@gmail.com"
password = "srty ivse sfsr gpmx"

# Email content
subject = "Your Personal Weather Report - SMTP."

# Setting up the SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # For SSL
server.login(sender_email, password)

# Creating the email message
emailbody = f"Subject: {subject}\n" + '\n\n'.join(allparagraphs)

# Sending the email
x = server.sendmail(sender_email, receiver_email, emailbody)
server.quit()

print("Email sent successfully!")

#******************************************
"""""
# Code to send slack message.

# Still gettin error message on line - client = WebClient(token=SLACK_API_TOKEN) # getting error msg on WebClient
kKept in file to show you how far I was in that portion of the project.


# Define your Slack API token
SLACK_API_TOKEN = "xoxe.xoxp-1-Mi0yLTMxODc1NDA3NDA0OC02NzczODgwODk1NjM1LTY5MjIxMDk0OTMwNTktNjkxOTMwODMxMjgwNS0wNjNkMjBlZjVhYTA5MDVkZTk0NjFiMzdhMDM3MzQ3MDA1ZWY4MDBkYTg3N2NlZWNjMWRiM2E5ZDFmZDRhZTgz"

# Initialize a WebClient instance
client = WebClient(token=SLACK_API_TOKEN) # getting error msg on WebClient

# channel_id = input("Enter your email address e.g., yourname@example.com): ")

# Define the channel and message
channel_id = "#interns-q1-2024"
# message = "Hello from Python!" COMMENTED OUT - USING allparagraphs

try:
    # Send the message
    response = client.chat_postMessage(channel="interns-q1-2024", text=allparagraphs)
    print("Message sent successfully:", response["ts"])
except SlackApiError as e:
    # Print any errors
    print("Error sending message:", e.response["error"])
"""