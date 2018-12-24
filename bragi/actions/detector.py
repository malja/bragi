import cv2
import os
import numpy as np
import argparse
import uuid
import time
import datetime
import math

from bragi import Config

class Detector:
    def __init__(self, input_path: str, config: Config):
        self.input_video_path = input_path
        self.config = config
        self.video_capture = None
        self.classifiers = []
        self.time_start = None
        self.frames_count = 0
        self.frame_current = 0
        self.duration = None

    def __enter__(self):
        if not os.path.isfile(self.input_video_path):
            raise FileNotFoundError("Input video doesn't exist.")
        
        self.video_capture = cv2.VideoCapture(self.input_video_path)
        self.frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        for classifier_path in self.config.detection.classifiers:
            self.classifiers.append(
                cv2.CascadeClassifier()
            )

            if not self.classifiers[-1].load(classifier_path):
                raise RuntimeError("Classifier '{}' couldn't be loaded.".format(classifier_path))    

        return self

    def __exit__(self, exception_type, value, traceback):
        self.video_capture.release()

    def detect(self):
        # Read video if available
        while self.video_capture.isOpened():

            # Get one frame
            ret, frame = video.read()

            # On error
            if not ret:
                raise RuntimeError("Unable to read video frame.")

            # Skip some frames to process it faster
            self.frame_current += 1
            if frame_current % self.config.detection.skip_frames != 0:
                continue

            # Calculate duration time
            if self.frame_current % 500 == 0:
                elapsed = time.time() - timer_start
                self.timer_start = time.time()
                self.duration = datetime.timedelta(seconds=math.floor((self.frames_count - self.frame_current) / 500 * elapsed))

            # Detect faces in grayscale image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            all_faces = []
            for classifier in self.classifiers:
                faces = classifier.detectMultiScale(gray, scaleFactor=self.config.detection.scale_factor, minNeighbors=self.config.detection.min_neighbors)
                if len(faces) != 0:        
                    for face in faces:
                        x,y,w,h = face
                        all_faces.append(
                            frame[y:y+h, x:x+w]
                        )

            if len(all_faces) != 0:
                yield all_faces



# ----
"""

if not os.path.exists(args.input):
    print("Input file {} does not exist!".format(args.input))
    exit(1)

video = cv2.VideoCapture(args.input)
frames_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_current = 0

classifiers_sources = [
    "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml",
    "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_profileface.xml",
    "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml",
    "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_frontalface_improved.xml",
]

# "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml",
# "C:/Users/janma/Documents/opencv/sources/data/haarcascades/haarcascade_profileface.xml"

# "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_profileface.xml",
# "C:/Users/janma/Documents/opencv/sources/data/lbpcascades/lbpcascade_frontalface_improved.xml",

classifiers = []
for classifier_source in classifiers_sources:
    classifiers.append(
        cv2.CascadeClassifier()
    )

# cv2.CascadeClassifier()

for index, classifier in enumerate(classifiers):
    if not classifier.load(classifiers_sources[index]):
        print("Unable to load classifiers.")
        exit(2)

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
                cv2.imwrite("{}.png".format(
                    os.path.join(args.output, "face_" + uuid.uuid4().hex)
                ), frame[y:y+h, x:x+w])

        break

video.release()
cv2.destroyAllWindows()
"""