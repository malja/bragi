import cv2
import numpy as np
import os
import sqlite3

class Recognizer:
    def __init__(self, config):

        self.config = config
        self.sqlite_connection = None
        self.sqlite_cursor = None

        self.face_recognizer = None
        self.people = []

    def setup(self):
        if not self._setup_database() or not self._setup_model():
            return False

    def _setup_database(self):
        try:
            # TODO: File with all path constants.
            self.sqlite_connection = sqlite3.connect("./dataset/dataset.db")
            self.sqlite_connection.row_factory = sqlite3.Row
            self.sqlite_cursor = self.sqlite_connection.cursor()
        except Exception as e:
            print("Error: {}".format(e))
            return False

        return True

    def _setup_model(self):
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Either load already created model

        # TODO: Create file with all path constants
        if not os.path.isfile("./dataset/model.xml"):
            if not self.create_model():
                print("Error: There was no model and it's creation failed.")
                return False

        if not self.face_recognizer.load("./dataset/model.xml"):
            print("Error: Could not load model")
            return False
        
        return True


    def create_model(self):
        self.sqlite_cursor.execute("SELECT id, first_name, last_name FROM `people`")
        records = self.sqlite_cursor.fetchall()

        photos = []
        labels = []

        for record in records:
            # TODO: File with path constants
            photo_files = [ item for item in os.listdir("./dataset/person_{}".format(record["id"])) ]

            for photo_file in photo_files:
                photos.append(
                    # TODO: Make Detector save grayscale images
                    cv2.cvtColor(
                        cv2.imread(
                            os.path.join("./dataset/person_{}".format(record["id"]), photo_file)
                        ), cv2.COLOR_BGR2GRAY
                    )
                )
        
            labels.append(record["id"])

            if record["id"] not in self.people: 
                name = "{last}, {first}".format(
                    last = record["last_name"],
                    first = record["first_name"]
                )
                self.people[record["id"]] = name

        self.face_recognizer.train(photos, np.array(labels))

        # TODO: File with path constants
        if not self.face_recognizer.save("./dataset/model.xml"):
            return False

        return True
        

    def recognize(self, face):
        face_id, confidence = self.face_recognizer.predict(face)
                
        if confidence < self.config.recognition.min_confidence:
            # TODO: Return class Person!!!
            return -1

        return face_id


"""
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
"""