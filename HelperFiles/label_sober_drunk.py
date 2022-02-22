import os

for infile in os.listdir("./"):
     #print("file : " + infile)
     if '_1_F' in infile.upper():
         print("sober" + infile)
     elif  infile[-2:] == "py": #include any other files you don't want to delete lol
         print(infile)
     else:
         print("drunk" + infile)