# Codejam12-StayAwake

# First place overall at McGill EUS Codejam 12!!

## Necessary Downloads and Imports
- flask
- pandas
- pyodbc
- mediapipe
- opencv-python
- geocoder
- playsound
- pyttsx3
- [ODBC Driver 18 for for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)

## Inspiration
According to the NSC, roughly 18% of truck drivers report falling asleep behind the wheel, and drowsy driving could be involved in upwards of 40% of truck crashes. Drowsiness while driving is hazardous for carriers and surrounding drivers. Keeping carriers awake and alert could save lives.
We hope to develop a product to ensure the safety of carriers behind the wheel and provide analytics to avoid driving fatigue by smarter route and schedule planning 

## What it does
Real-time face mesh detection and landmark extraction using OpenCV2 and mediapipe->Eye aspect ratio (EAR) calculated per frame indicates drowsiness, triggering alarm when needed->Storage of geographical information (lat. & long.) in SQL server where carriers frequently fall asleep->Arrange stops before high-risk segments or adjust schedule accordingly

## How we built it
App development in Flask, HTML, and CSS. Eye recognition and drowsiness detection using OpenCV2 and Mediapipe. Data storage in Microsoft Azure SQL Server database.

## Challenges we ran into
Frontend and UI design, machine learning model deployment, database connection 

## What's next for Stay Awake
Stay tuned!
