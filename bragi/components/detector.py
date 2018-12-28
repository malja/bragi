import cv2
import numpy as np
import time
import datetime
import math
import os

from bragi import Config

class Detector:
    """
    Detect faces in given video. 

    It goes through the video frame by frame (or skips every `config.detection.skip_frames`) and detect all faces.
    Classifiers defined in `config.detection.classifiers` are used. When any number of faces is detected in frame,
    array containing all of them is yield-ed from `detect` method.

    Usage:
    ======

        with Detector("path_to_video", config_object) as d:
            for faces in d.detect():
                for face in faces:
                    # ... do something with face

    """

    def __init__(self, input_path: str, config: Config):
        """
        Setup detector input and configuration.
        :param str input_path: Path to video in which faces should be detected.
        :param bragi.Config config: Configuration.
        """

        self.input_video_path = input_path  # Path to the video
        self.config = config                # Config's instance
        self.video_capture = None           # cv2.VideoCapture's instance
        self.classifiers = []               # List of cv2.CascadeClassifiers' instances
        self.time_start = None              # Time when detection started
        self.frames_count = 0               # Total number of frames in video
        self.frame_current = 0              # Current frame number
        self.duration = None                # Expected duration as string

    def __enter__(self):
        if not os.path.isfile(self.input_video_path):
            raise FileNotFoundError("Input video doesn't exist.")
        
        self.video_capture = cv2.VideoCapture(self.input_video_path)
        self.frames_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

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
            ret, frame = self.video_capture.read()

            # On error
            if not ret:
                raise RuntimeError("Unable to read video frame.")

            # Skip some frames to process it faster
            self.frame_current += 1
            if self.frame_current % self.config.detection.skip_frames != 0:
                continue

            # Calculate duration time
            if self.frame_current % 500 == 0:
                elapsed = time.time() - self.time_start
                self.timer_start = time.time()
                self.duration = datetime.timedelta(seconds=math.floor((self.frames_count - self.frame_current) / 500 * elapsed))

            # cv2 detection works only on grayscale image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            all_faces_in_frame = []

            # Detect with all classifiers
            for classifier in self.classifiers:
                faces = classifier.detectMultiScale(gray, scaleFactor=self.config.detection.scale_factor, minNeighbors=self.config.detection.min_neighbors)
                for face in faces:
                    x,y,w,h = face

                    # Ignore small faces
                    if w < self.config.detection.output.min_width or h < self.config.detection.output.min_height:
                        continue

                    all_faces_in_frame.append(
                        frame[y:y+h, x:x+w]
                    )

            if len(all_faces_in_frame) != 0:
                yield all_faces_in_frame


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