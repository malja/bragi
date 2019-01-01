import cv2
import os

from bragi import Constants

files = [ os.path.join(Constants.PATH_FACES, name) for name in os.listdir(Constants.PATH_FACES) ]

for file_name in files:
    face = cv2.imread(file_name)
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(file_name, gray)
