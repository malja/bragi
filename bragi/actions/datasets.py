import sqlite3
import argparse
import os
import cv2
import uuid
import shutil

parser = argparse.ArgumentParser(description="Generate datasets from detected faces.")
parser.add_argument("database", help="Path to database file.")
parser.add_argument("faces", help="Path to directory with faces.")

args = parser.parse_args()

if not os.path.exists(args.faces):
    print("Directory with faces does not exist.")
    exit(1)

if not os.path.exists(args.database):
    create_tables = True
else:
    create_tables = False

try:
    connection = sqlite3.connect(args.database)
    cursor = connection.cursor()
except Exception as e:
    print(e)
    exit(2)


if create_tables:
    try:
        print("Creating tables...")
        cursor.execute("CREATE TABLE `faces` (`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, `uuid`	TEXT UNIQUE, `name`	TEXT NOT NULL, `folder`	TEXT NOT NULL)")
        connection.commit()
    except Exception as e:
        print("Could not create table `faces`. E: {}".format(e))
        exit(3)

face_files = [ item for item in os.listdir(args.faces) if os.path.isfile(os.path.join(args.faces, item)) ]

face_name = input("Face name: ")
cursor.execute("SELECT uuid, name, folder FROM `faces` WHERE `name` LIKE ?", (face_name,))
connection.commit()
record = cursor.fetchone()

face_id = 0
face_folder = ""

if not record:
    create_new = input("Person does not exist. Create new? [Y/n]: ")

    if create_new == "Y" or create_new == "y" or create_new == "":
        face_id = uuid.uuid4().hex
        face_folder = os.path.join(os.path.dirname(args.database), "person_{}".format(face_id))
        cursor.execute("INSERT INTO `faces` (uuid, name, folder) VALUES (?, ?, ?)", (face_id, face_name, face_folder))
        connection.commit()
    else:
        exit(0)
else:
    face_id, face_name, face_folder = record
    use_face = input("Found existing record: {}. Is it ok? [Y/n]: ".format(face_name))
    if use_face != "Y" and use_face != "y" and use_face != "":
        create_new = input("Create as new record? [Y/n]: ")
        if create_new == "Y" or create_new == "y" or create_new == "":
            face_id = uuid.uuid4().hex
            face_folder = os.path.join(os.path.dirname(args.database), "person_{}".format(face_id))
            cursor.execute("INSERT INTO `faces` (uuid, name, folder) VALUES (?, ?, ?)", (face_id, face_name, face_folder))
            connection.commit()
        else:
            exit(0)

print("Using ID={}, Face={}".format(face_id, face_name))

if not os.path.exists(face_folder):
    os.mkdir(face_folder)

num_of_faces = len(face_files)
current_face_index = 0

print("Press 'y' for adding face to '{}'".format(face_name))
print("Press 'x' deleting face. For example remove images without face.")
print("Press 'n' to skip this face. Assign it to different person later.")

for face_file in face_files:

    current_face_index += 1

    print("Face: {}/{}".format(current_face_index, num_of_faces), end="\r")

    face_file_source = os.path.join(args.faces, face_file)
    face_file_destination = os.path.join(face_folder, face_file)

    face = cv2.imread(face_file_source)

    cv2.namedWindow("Face", cv2.WINDOW_NORMAL)
    cv2.imshow("Face", face)
    key = cv2.waitKey(0)

    if chr(key & 255 ) == "y":
        shutil.move(face_file_source, face_file_destination)
    elif chr(key & 255) == "n":
        continue
    elif chr(key & 255) == "x":
        os.remove(face_file_source)

    cv2.destroyAllWindows()