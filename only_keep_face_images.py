import os

for infile in os.listdir("./"):
     #print("file : " + infile)
     if '_F_F' in infile.upper() or '_F_M' in infile.upper():
         print(infile)
     elif  infile[-2:] == "py": #include any other files you don't want to delete lol
         print(infile)
     else:
         os.remove(infile)