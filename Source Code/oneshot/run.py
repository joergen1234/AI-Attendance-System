import pandas as pd
import cv2
import csv
import numpy as np
import face_recognition
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
import requests
from firebase_admin import firestore
import json
api = "https://script.google.com/macros/s/AKfycbzoLuEnoQMmCsx6S6ojiOD4Lhvb717U_v6JqqCJ3s2eBvybuHBqOrxyCu7RZmlhK6xP3w/exec"
# Use a service account.
cred = credentials.Certificate(
    'classapp-bea16-firebase-adminsdk-jail9-c892accbdb.json')
 
 
app = firebase_admin.initialize_app(cred)

db = firestore.client()
ct = datetime.now().day
day = ct % 7
li = ["Sunday", "Monday", "Tuesday", "Wednesday",
      "Thursday", "Friday", "Saturday",]
d = li[day]

email = "dypiemr19@gmail.com"


def fetchcloud():
    crtime = datetime.now().strftime("%I:%M")

    if (int(datetime.now().strftime("%I")) < 10):
        crtime = crtime[1:]
    users_ref = db.collection(u'users').document(
        email).collection(u'web').document(u'docu')

    docs = users_ref.get()
    if docs.exists:
        a = docs.to_dict()
        cname = a['customname']
        subref = db.collection(u'users').document(
            email).collection(u'timetables').document(cname).collection(d).stream()
        subject = ""
        for doc in subref:
            dt = doc.to_dict()
            st = dt['startTime']
            et = dt['endTime']
            if (crtime >= st and crtime <= et):
                subject = dt['subject']
                return subject
    else:
        return None


def uploadCount(cnt):

    data = {
        u'count': cnt
    }
    db.collection(u'users').document(
        email).collection(u'web').document(u'docu').update(
        data
    )


df = pd.DataFrame(columns=['Name', 'Time', 'Subject'])
timing = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
df.to_csv('G:\oneshot\Attendance\Attendance_'+timing+'.csv', index=False)


path = r'G:\oneshot\Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def send_data(link, params):
    headers = {
        "Content-Type": "application/json"
    }
    json_data = json.dumps(params)

    res = requests.post(link, json_data, headers=headers)

    if res.status_code == 200:
        # Print the response content
        print(res.content)
    else:
        # Print the error message
        print("Error:", res.status_code, res.text)


def markAttendance(name):
    with open(r'G:\oneshot\Attendance\Attendance_'+timing+'.csv', 'r+') as f:
        myDataList = f.readlines()

        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            subject = fetchcloud()
            send_data(
                api, {"id": name+dtString, 'name': name, 'date': dtString, 'subject': subject})
            f.writelines(f'\n{name},{dtString},{subject}')


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

df = pd.read_csv('G:\oneshot\Attendance\Attendance_'+timing+'.csv')
num_rows, num_cols = df.shape
uploadCount(num_rows)
print("Total number of present students for current class: ", num_rows)
