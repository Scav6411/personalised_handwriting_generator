# -*- coding: utf-8 -*-
"""easy_ocr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KK4uNn89w772YriNuIaYMSP1ITaBU72w
"""


import easyocr
import cv2
from PIL import Image
import os

class EasyOCR():
  def __init__(self,image_path):
    self.image_path = image_path
    self.id = 0
    self.forward(self.image_path)

  def get_boxes(self):
    bro = easyocr.Reader(['ch_sim','en'])
    result = bro.readtext(self.image_path)
    boxes=[]
    elements=[]
    for element in result:
      for a in element:
        elements.append(a)
        break

    for coord in elements:
      boxest=[]
      a=[]
      b=[]
      c=[]
      d=[]
      count=0
      for row in coord:
        if(count==0):
          a=row
        elif(count==1):
          b=row
        elif(count==2):
          c=row
        else:
          d=row
        count=count+1
      if(a[0]==b[0] or a[0]==c[0] or a[0]==d[0]):
          startx=(min(a[0],min(b[0],min(c[0],d[0]))))
          boxest.append(startx)
          starty=(min(a[1],min(b[1],min(c[1],d[1]))))
          boxest.append(starty)
          endx=(max(a[0],max(b[0],max(c[0],d[0]))))
          boxest.append(endx)
          endy=(max(a[1],max(b[1],max(c[1],d[1]))))
          boxest.append(endy)
          boxes.append(boxest)
    return boxes

  def get_coordinates(self,boxes):
    results = []
    image = cv2.imread(self.image_path)

    #Saving a original image and shape
    orig = image.copy()

    # loop over the bounding boxes to find the coordinate of bounding boxes
    for (startX, startY, endX, endY) in boxes:

      r = orig[startY:endY, startX:endX]
      #configuration setting to convert image to string.
      configuration = ("-l eng --oem 1 --psm 8")

        ##This will recognize the text from the image of bounding box

      # append bbox coordinate and associated text to the list of results
      results.append((startX, startY, endX, endY))

    #Display the image with bounding box and recognized text
    orig_image = orig.copy()

    # plt.imshow(orig_image)
    # plt.title('Output')
    # plt.show()

    pil_image = Image.fromarray(orig_image)

    # Save the image as JPEG
    save_path = "BoxImage.jpg"
    pil_image.save(save_path, "JPEG")
    return results

  def img_cropper(self,results):
    # Specify the path and name of the new folder
    #Saving a original image and shape
    orig = cv2.imread(self.image_path)
    orig_image = orig.copy()
    folder_path = '/content/Cropped_Images'
    id=0
    # Check if the folder was created
    if os.path.exists(folder_path):
        print("Cropped_Images folder already exists.")
    else:
        # Create the new folder
        os.makedirs(folder_path)
        print("Cropped_Images folder created successfully.")
    # Loop over the bounding boxes to crop the image
    for i, ((startX, startY, endX, endY)) in enumerate(results):
        # Crop the image using the bounding box coordinates
        cropped_image = orig_image[startY:endY, startX:endX]

        # Create a PIL image from the cropped image array
        pil_image = Image.fromarray(cropped_image)

        #Create ids for _getitem_() function
        id=id+1
        #Save the cropped image with a unique name
        save_path = f"/content/Cropped_Images/Cropped_Images_{i+1}.jpg"
        pil_image.save(save_path)

        # #Display the cropped image
        # plt.imshow(pil_image)
        # plt.title(f"Cropped Image {i+1}")
        # plt.show()
    return id

  def forward(self,images):
    boxes = self.get_boxes()
    results = self.get_coordinates(boxes)
    self.id = self.img_cropper(results)
    return id, print('Words are extracted from the input image.')