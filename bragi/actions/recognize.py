import cv2
import numpy as np
import argparse
import os
import sqlite3
import time
import datetime
import math

parser = argparse.ArgumentParser(description="Recognize people in video base on provided dataset.")
parser.add_argument("dataset", help="Path to dataset directory.")
parser.add_argument("video", help="Path to video.")
args = parser.parse_args()

dataset_db_file = os.path.join(args.dataset, "datasets.db")

if not os.path.exists(args.video):
    print("Video does not exist.")
    exit(1)

if not os.path.isdir(args.dataset):
    print("Dataset directory does not exist.")
    exit(2)

if not os.path.exists(dataset_db_file):
    print("Database file is not found.")
    exit(2)

try:
    connection = sqlite3.connect(dataset_db_file)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
except Exception as e:
    print("Cannot connect to database. E: {}".format(e))
    exit(3)

cursor.execute("SELECT id, name, folder FROM `faces`")
records = cursor.fetchall()

photos = []
labels = []
names = {}

for record in records:
    print("Loading photos for {}...".format(record["name"]))
    photo_files = [ item for item in os.listdir(os.path.join(args.dataset, record["folder"])) ]

    for photo_file in photo_files:
        photos.append(
            cv2.cvtColor(
                cv2.imread(
                    os.path.join(args.dataset, record["folder"], photo_file)
                ), cv2.COLOR_BGR2GRAY
            )
        )
        labels.append(record["id"])
        if record["id"] not in names:
            names[record["id"]] = record["name"]

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# TODO load from xml! Build recognizers in separate step

face_recognizer.train(photos, np.array(labels))

# .................................................

video = cv2.VideoCapture(args.video)
frames_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_current = 0

classifiers_sources = [
    "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml",
    "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_profileface.xml",
    "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml",
    "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_frontalface_improved.xml",
]

classifiers = []
for classifier_source in classifiers_sources:
    classifiers.append(
        cv2.CascadeClassifier()
    )

for index, classifier in enumerate(classifiers):
    if not classifier.load(classifiers_sources[index]):
        print("Unable to load classifiers.")
        exit(4)

print("Frame: {}/{}".format(0, frames_total), end="\r")

timer_start = time.time()
duration = "Calculating ..."

while(video.isOpened()):
    ret, frame = video.read()

    if not ret:
        break

    frame_current += 1

    if frame_current%10 != 0:
        continue

    if frame_current%500 == 0:
        elapsed = time.time() - timer_start
        timer_start = time.time()
        duration = datetime.timedelta(seconds=math.floor((frames_total - frame_current) / 500 * elapsed))

    print("Frame: {}/{}. Duration: {}".format(frame_current, frames_total, duration), end="\r")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for classifier in classifiers:
        faces = classifier.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if len(faces) != 0:        
            for face in faces:
                x,y,w,h = face
                
                label = face_recognizer.predict(gray[y:y+h, x:x+w])
                
                if label[1] > 50:
                    continue

                label = label[0]

                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 234, 0), 2)
                cv2.putText(frame, names[label], (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,0), 1)
                cv2.imshow(names[label], frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                print("Recognized id={}, name={}".format(label, names[label]))

        break

video.release()
