import os
from PIL import Image


for infile in os.listdir("./"):
    print("file : " + infile)
    if infile[-3:] == "tif" or infile[-3:] == "bmp" :
       # print "is tif or bmp"
       outfile = infile[:-3] + "jpeg"
       im = Image.open(infile)
       print("new filename : " + outfile)
       out = im.convert("RGB")
       out.save(outfile, "JPEG", quality=90)