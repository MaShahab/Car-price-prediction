import requests
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import mysql.connector
import csv
import unicodecsv
from sklearn import tree


functionsList = list()
pricesList = list()
citiesList = list()
citiesListX = list()
carModelList = list()
carModelListX = list()
totalList = list()
tupplesList = list()

url_input = input('Enter a <<BAMA>> website cars serch link : ')

r = requests.get(url_input)
soup = BeautifulSoup(r.text,'html.parser')


fVal = soup.find_all('p',attrs={'class':'price hidden-xs'})

for i in range(0,len(fVal)):
    functionsList.append(fVal[i].text)
    totalList.append(fVal[i].text)
    i +=1


pVal = soup.find_all('span',attrs={'itemprop':'price'})

for l in range(0,len(pVal)):
    pricesList.append(pVal[l].text)
    totalList.append(pVal[l].text)
    l +=1


cVal = soup.find_all('span',attrs={'class':'provice-mobile'})

for c in range(0,len(cVal)):
    citiesList.append(cVal[c].text)
    totalList.append(cVal[c].text)


mval = soup.find_all('h2',attrs={'class':'persianOrder'})

for m in range(0,len(mval)):
    carModelList.append(mval[m].text)
    m +=1

for q in range(0,len(mval)):
    carModelListX.append(re.sub(r'\s+',' ', carModelList[q]).strip())
    totalList.append(re.sub(r'\s+',' ', carModelList[q]).strip())
    q +=1


dictionary = OrderedDict(zip(pricesList,functionsList))


dictlen = len(dictionary)

cnx = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='py_learning')
cursor = cnx.cursor()

# print(list(dictionary.keys())[0])

# print(carModelListX)

for i in range(0,dictlen):
    # print(list(dictionary.keys())[i])
    # print(list(dictionary.values())[i])
    cursor.execute("INSERT INTO bama VALUES (%s, %s, %s)", ( list(dictionary.keys())[i] , list(dictionary.values())[i] , carModelListX[i] ))
cnx.commit()


query = 'SELECT * FROM bama;'
cursor.execute(query)
write_file = 'records.csv'
with open(write_file, "w") as output:
    for l in cursor:
        # print(l)
        tupplesList.append(l)
        # output.write(l[0])
        # output.write(l[2])
        
print(tupplesList)


with open('records.csv','w',newline='',encoding='utf-8') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['function','price','model'])
    for row in tupplesList:
        csv_out.writerow(row)


x = [] #input data's
y = [] #output data's

with open('records.csv','r') as csvfile:
    data = csv.reader(csvfile)
    for line in tupplesList:
        x.append(line[1:3])
        y.append(line[0])

# print(x)
# print(y)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)
new_data = [['','']]                  #Here is where we should enter new data
answere = clf.predict(new_data)
print(answere)