#pip install translate
import scipy.io as sio
import pandas as pd


mat_file = sio.loadmat('ALLDATA2.mat', struct_as_record = False, squeeze_me = True) #loaded as a dictionary

new_shit = []

for i in mat_file['ALLDATA2']:
    #print(i[0:9])
    new_shit.append(i[0:10])

dict_format = {}
dict_keys = []
dict_vals = []

#translator= Translator(from_lang = "spanish" , to_lang="English")
all_vals = []

for x in range(0,10):
    row_val =[]
    for i in new_shit[x]:
        row_val.append(i)
    all_vals.append(row_val)

data = all_vals[1:10]

df_clean = pd.DataFrame(data, columns = ['Name', 'Age', 'Height', 'Weight', 'Sex', 
                                   'Alcohol Test 1','Alcohol Test 2','Alcohol Test 3','Alcohol Test 4', 'Alcohol Test 5'])

print(df_clean)

df_clean.to_csv('picture_meta_data.csv')


# Dictionary Keys
#__header__
#__version__
#__globals__
#ALLDATA2 #only important one # data type - numpy.ndarray

'''
['Nombre'] [0] # name
['edad'] [1]] # age
['altura'] [2] # height
['peso'] [3] # weight
['sexo(1H-0M)'] [4] # sex - 1 = male,0 = female
['Alcotest1'] [5] # alcohol test 1
['Alcotest2'] [6] # alcohol test 2
['Alcotest3'] [7] # alcohol test 3
['Alcotest4'] [8] # alcohol test 4
['Alcotest5'] [9] # alcohol test 5
['Adquisicion 1'] [10] # picture capture 1
['Adquisicion 2'] [11] # picture capture 2
['Adquisicion 3'] [12] # picture capture 3
['Adquisicion 4'] [13] # picture capture 4
['Adquisicion 5'] [14] # picture capture 5'''
