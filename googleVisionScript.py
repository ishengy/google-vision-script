# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:08:52 2019

@author: ivan.sheng
"""

from google.cloud import storage
from google.cloud import vision
import pandas as pd
import os

path = 'C:/Users/ivan.sheng/Downloads/'
os.chdir(path)

key = 'New Biz-ceb0200cadc9.json'
gs = 'gs://control-is/'

client = storage.Client.from_service_account_json(key)
bucket = client.get_bucket('control-is')

uri_list = []

for blobs in bucket.list_blobs():
    uri_list.append(gs + blobs.name)    

fileName = []
mid = []
description = []
score = []

ImageLabels = pd.DataFrame()

client = vision.ImageAnnotatorClient.from_service_account_json(key)
image = vision.types.Image()

#count = 0
#test = "gs://espresso-is/55872696_377592346176898_2661589277612575819_n.jpg"
#
#image.source.image_uri = test
#response = client.face_detection(image=image)
#faces = response.face_annotations
#
#print(len(faces))
#print(len(faces[0].landmarks))
#print(faces[0].landmarks[33].type)
#print(faces[0].landmarks[0].position.x) #store y and z as well
#print(faces[0].headwear_likelihood)

joy = []
sorrow = []
anger = []
surprise = []
exposed = []
blurred = []
headwear = []

#for loop from bottom down
count = 0
for uri in uri_list:
    image.source.image_uri = uri
    response = client.face_detection(image=image)
    faces = response.face_annotations
    
    for i in range(0,len(faces)):
        fileName.append(uri)    
        joy.append(faces[i].joy_likelihood) # Store MID
        sorrow.append(faces[i].sorrow_likelihood) # Store label
        anger.append(faces[i].anger_likelihood)
        surprise.append(faces[i].surprise_likelihood) # Store score of label
        exposed.append(faces[i].under_exposed_likelihood)
        blurred.append(faces[i].blurred_likelihood)
        headwear.append(faces[i].headwear_likelihood)
    
    count = count+1
    print(count)
count = 0    
#end for loop


#for loop from bottom down
count = 0

for uri in uri_list:
    image.source.image_uri = uri
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    for i in range(0,len(labels)):
        fileName.append(uri)    
        mid.append(labels[i].mid) # Store MID
        description.append(labels[i].description) # Store label
        score.append(labels[i].score) # Store score of label
    
    count = count+1
    print(count)
count = 0    
#end for loop

ImageLabels['Image'] = fileName
ImageLabels['Joy'] = joy
ImageLabels['Sorrow'] = sorrow
ImageLabels['Anger'] = anger
ImageLabels['surprise'] = surprise
ImageLabels['Exposed'] = exposed
ImageLabels['Blurred'] = blurred
ImageLabels['Headwear'] = headwear

out = pd.ExcelWriter('nespresso_imgface.xlsx')
ImageLabels.to_excel(out,'nespresso')
out.save()