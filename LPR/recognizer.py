import cv2
import pytesseract
import numpy as np
import os

def get_lic(image):

    pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    xml_path = os.path.join(os.path.dirname(__file__), 'haarcascade_russian_plate_number.xml')  
    
    cascade=cv2.CascadeClassifier(xml_path)

    states_code={ "MH" : "Maharashtra", "GA" : "Goa", "GJ" : "Gujarat", "DL" : "Delhi", "UP" : "Uttar Pradesh" }

    img_1=cv2.imread(image)
    gray=cv2.cvtColor(img_1,cv2.COLOR_BGR2GRAY)
    num_plate=cascade.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in num_plate:

        a,b=(int(0.02*img_1.shape[0]), int(0.025*img_1.shape[1]))
        plate=gray[y+a:y+h-a,x+b:x+w-b]

        height, width = plate.shape[:2]
        newWidth = int(width * 1.2)
        newHeight = int(height * 1.2)
        plate = cv2.resize(plate, (newWidth, newHeight))

        ker=np.ones((1,1),np.uint8)
        plate=cv2.dilate(plate,ker,iterations=1)
        plate=cv2.erode(plate,ker,iterations=1)
        (thresh, plate)=cv2.threshold(plate,127,255,cv2.THRESH_BINARY)

        read=pytesseract.image_to_string(plate)
        read=''.join(e for e in read if e.isalnum())
        sta=read[0:2]
        try:
            print("Car is from ", states_code[sta])
        except:
            print('State not present!!')
            
        cv2.rectangle(img_1,(x,y),(x+w ,y+h),(51,51,255),2)
        cv2.rectangle(img_1,(x,y-40),(x+w,y),(51,51,255),-1)
        cv2.putText(img_1,read,(x,y-10),cv2.FONT_HERSHEY_PLAIN,1.5,(255,255,255),2)

    cv2.imwrite(image,img_1)
    return read

#Notes:
'''
Since media is stored locally, we can directly update file and save to the same location. The model does not need to be updated.
Django uses file pointer to point to the saved media of a model. 
Since we overwrite the image in the same location where the file pointer points, the updated image is shown.
'''