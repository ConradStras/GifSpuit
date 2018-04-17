import glob
import os
import cv2

# -*- coding: utf-8 -*-

import numpy as np
from os import walk, getcwd
from PIL import Image

classes = ["sunflower"]
"""-------------------------------------------------------------------"""

""" Configure Paths"""
mypath = "/home/conrad/PyCharmProjects/Gifspuitwork/sunflowertextsoriginal/"
outpath = "/home/conrad/PyCharmProjects/Gifspuitwork/sunflowerxmls/"


cls = "sunflower"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt' % (wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
txt_name_list.sort()
print(txt_name_list)

# convert text string to a list of XML
# we feed the directory of the file to create an xml into this function
def create_xml(txtpath,txtname,w, h):
    xmls = []
    txt_file = open(txtpath,"r")
    lines = txt_file.read().split('\n')  # for ubuntu, use "\r\n" instead of "\n"
    ct = 0
    for line in lines:
        if len(line) == 0:
            xmls.append('</annotation>\n')
            break
        if len(line) <=2 and line != '':
            xmls.append('<annotation>\n')
            xmls.append('\t<folder>VOC2007</folder>\n')
            xmls.append('\t<filename>' + txtname.split('.')[0] + '.JPEG</filename>\n')
            xmls.append('\t<source>\n')
            xmls.append('\t\t<database>The VOC2007 Database</database>\n')
            xmls.append('\t\t<annotation>PASCAL VOC2007</annotation>\n')
            xmls.append('\t\t<image>flickr</image>\n')
            xmls.append('\t\t<flickrid>192073981</flickrid>\n')
            xmls.append('\t</source>\n')
            xmls.append('\t<owner>\n')
            xmls.append('\t\t<flickrid>tobeng</flickrid>\n')
            xmls.append('\t\t<name>Conrad Strasheim</name>\n')
            xmls.append('\t</owner>\n')
            xmls.append('\t<size>\n')
            xmls.append('\t\t<width>' + str(w) + '</width>\n')
            xmls.append('\t\t<height>' + str(h) + '</height>\n')
            xmls.append('\t\t<depth>3</depth>\n')
            xmls.append('\t</size>\n')
            xmls.append('\t<segmented>0</segmented>\n')
            boxes = int(line)
        elif len(line) >= 3:
            object_name = classes[0]
            x_min = line.split(' ')[0]
            y_min = line.split(' ')[1]
            x_max = line.split(' ')[2]
            y_max = line.split(' ')[3]
            xmls.append('\t<object>\n')
            xmls.append('\t\t<name>sunflower</name>\n')
            xmls.append('\t\t<pose>Left</pose>\n')
            xmls.append('\t\t<truncated>0</truncated>\n')
            xmls.append('\t\t<difficult>0</difficult>\n')
            xmls.append('\t\t<bndbox>\n')
            xmls.append('\t\t\t<xmin>'+x_min+'</xmin>\n')
            xmls.append('\t\t\t<ymin>'+ y_min + '</ymin>\n')
            xmls.append('\t\t\t<xmax>' + x_max + '</xmax>\n')
            xmls.append('\t\t\t<ymax>' + y_max + '</ymax>\n')
            xmls.append('\t\t</bndbox>\n')
            xmls.append('\t</object>\n')
    txt_file.close()
    return xmls

image = cv2.imread("/home/conrad/PyCharmProjects/Gifspuitwork/sunflowerimages/0001.JPEG")
h = image.shape[0]
w = image.shape[1]

# write a list of XML to file
def write_to_file(xmls, file_name):
    f = open(file_name, 'w')
    for line in xmls:
        f.write(line)
    f.close()

for k in txt_name_list:
    xml = create_xml(mypath+k, k, w, h)
    write_to_file(xml, k.split('.')[0] + '.xml')