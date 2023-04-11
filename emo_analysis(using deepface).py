import cv2
from deepface import DeepFace
import os
from PIL import Image

def is_notInterested(img_address="static/capture.jpg"):
    img = cv2.imread(img_address)
    result = DeepFace.analyze(img, actions = ['emotion'])
    print(result)
    not_interested=(result['emotion']['angry']+result['emotion']['disgust']+result['emotion']['fear']+result['emotion']['sad'])/4
    interested=(result['emotion']['happy']+result['emotion']['suprise']+result['emotion']['neutral'])/3
    if interested<not_interested:
        return True
    else:
        return False


static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
for i in range(1,6):
    img_add=os.path.join(static_folder, "img"+str(i)+".png")
    with Image.open(img_add) as image:
        width, height = image.size
    print(is_notInterested(img_add))
    print()
    