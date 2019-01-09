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
        self.duration = 15000                # Expected duration as string
        self._video_position = 0            # Number of seconds since video beginning
        self._video_fps = 0                 # FPS
        self._video_duration = 0            # Video length in seconds

    def __enter__(self):
        if not os.path.isfile(self.input_video_path):
            raise FileNotFoundError("Input video doesn't exist.")
        
        self.video_capture = cv2.VideoCapture(self.input_video_path)
        self.frames_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._video_fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self._video_duration = float(self.frames_count) / float(self._video_fps)

        for classifier_path in self.config.detection.classifiers:
            self.classifiers.append(
                cv2.CascadeClassifier()
            )

            if not self.classifiers[-1].load(classifier_path):
                raise RuntimeError("Classifier '{}' couldn't be loaded.".format(classifier_path))    

        return self

    def __exit__(self, exception_type, value, traceback):
        self.video_capture.release()

    def getCurrentPositionTime(self):
        return round(self.frame_current / self.frames_count * self._video_duration)

    def getVideoDuration(self):
        return self._video_duration

    def detect(self, grayscale=False):

        self.time_start = time.time()

        # Read video if available
        while self.video_capture.isOpened():

            # Get one frame
            ret, frame = self.video_capture.read()

            # On error
            if not ret:
                return

            # Skip some frames to process it faster
            self.frame_current += 1
            if self.frame_current % self.config.detection.skip_frames != 0:
                continue

            # Calculate duration time
            if self.frame_current % 100 == 0:
                elapsed = time.time() - self.time_start
                self.time_start = time.time()
                self.duration = datetime.timedelta(seconds=math.floor((self.frames_count - self.frame_current) / 100 * elapsed))

            print("Detecting: {}/{}. Expected duration: {}     ".format(self.frame_current, self.frames_count, self.duration), end="\r")

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

                    if grayscale:
                        all_faces_in_frame.append(
                            gray[y:y+h, x:x+w]
                        )
                    else:
                        all_faces_in_frame.append(
                            frame[y:y + h, x:x + w]
                        )

            if len(all_faces_in_frame) != 0:
                yield all_faces_in_frame
