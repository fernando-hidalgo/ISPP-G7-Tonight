import datetime
from django.shortcuts import render, get_object_or_404
import qrcode
import hashlib
import binascii
import hmac
import cv2
from proyecto.models import *

def generate_qr_test():
    input_data = "http://ev.us.es"
    qr = qrcode.QRCode(
            version=2,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(path)

def read_qr_test():
    filename = path
    image = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is not None:
        print("QRCode data:")
        print(data)
    else:
        print("There was some error")

def read_qr_cam_test():
    cap = cv2.VideoCapture(0)
    # initialize the OpenCV QRCode detector
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        # detect and decode
        data, vertices_array, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if vertices_array is not None:
            if data:
                print("QR Code detected, data:", data)
        # display the result
        cv2.imshow("img", img)
        # Enter q to Quit
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()