import re
import csv
import datetime


p1 = re.compile('(\d{1,2})(.+)(\d{2}\.\d{1})')
now = datetime.datetime.now()
time = str(now.hour)+""+str(now.minute)
CSVFile = open(time+'.csv','w')
csv_writer = csv.writer(CSVFile)
csv_writer.writerow(['number','name','templature'])
with open('re.txt','r+',encoding='UTF-8') as file:
    for line in file:
        if line != "":
            number = re.search(p1,line).group(1)
            name = re.search(p1,line).group(2)
            tem = re.search(p1,line).group(3)
            csv_writer.writerow([number,name,tem])
CSVFile.close()


