#!/usr/bin/env python
# coding: utf-8

# In[4]:


import re
import csv


# In[5]:


#import pandas as pd
#df = pd.read_csv(r'C:\Users\cshelton\Desktop\July_QA_Accuracy.csv') 
#df = df.iloc[6:]
#df


# In[12]:


#load your csv
def openCSV():

    csvData = []
#
    with open(r'C:\Users\cshelton\Desktop\test_run_QA.csv', newline='\n') as csvfile:

        data = csv.DictReader(csvfile)
        for row in data:
            csvData.append(row)
        return csvData


# In[13]:


matcher = re.compile(r"\d+(\s?|\s+)(\w+)?(\s?|\s+)-(\s?|\s+)\d+(\s?|\s+)(\w+)?(\s?|\s+)-(\s?|\s+)\d+")


# In[14]:


csvTasks = openCSV()

QATasks = []

for task in csvTasks:
    
    if "QA" in task["Task Name"]:
        QATasks.append(task)
        
print(len(QATasks))


# In[89]:


#For every cell that contains more than one QA content within the same row, for every /n(returned space) create new row 

QATasksFixed = []

copyCount = 0

for rowNumber in range(0, len(QATasks)):
    
    
    QAReturnNumbers = QATasks[rowNumber]["Notes"].split("\n")

    if len(QAReturnNumbers) > 1:
        
        copies = []

        for i in range(0, len(QAReturnNumbers)):
            

                
            newRow = QATasks[rowNumber].copy()
            newRow["Notes"] = QAReturnNumbers[i].replace(",", "")
            QATasksFixed.append(newRow)

        
    else:
        
        QATasks[rowNumber]["Notes"] = QATasks[rowNumber]["Notes"].replace(",", "")
        QATasksFixed.append(QATasks[rowNumber])
                
    
print("Th original number of projects QA'd is:",len(QATasks))
print(copyCount)
print("The new number of projects QA'd is:",len(QATasksFixed))
    


# In[90]:


#Grab all cells from Notes column that contains the following pattern "int - int - int" and 
#add "0-0-0" for all blank rows or unecessary content
for task in QATasksFixed:
    
    s = re.search(r"\d+(\s?|\s+)(\w+)?(\s?|\s+)-(\s?|\s+)\d+(\s?|\s+)(\w+)?(\s?|\s+)-(\s?|\s+)\d+", task["Notes"])
    if s != None:
        
        QAReturnNumbers = s.group()
        nums = re.findall("(\d+)", QAReturnNumbers)
        if len(nums) == 3:
            task["Notes"] = nums[0] + "-" + nums[1] + "-" + nums[2]
    
    else:
        
        task["Notes"] = "0-0-0"


# In[102]:


#remove all cells that contain "0-0-0", because it serves no purpose for us
filteredTasks = []

for task in QATasksFixed:
    if task["Notes"] != "0-0-0":
        filteredTasks.append(task)
        
print("The number of Projects QA'd is:",len(filteredTasks))


# In[92]:


#display results after removing 0-0-0
for task in filteredTasks:
    print(task["Notes"])


# In[93]:


#convert to pandas
#split pattern into their own columns 
import pandas as pd

data = {'Errors':[], 'Comments':[], 'Pages':[]}


for task in filteredTasks:
    splitList = task["Notes"].split('-');
    data['Errors'].append(splitList[0])
    data['Comments'].append(splitList[1])
    data['Pages'].append(splitList[2])

QA_stuff = pd.DataFrame (data, columns = ['Errors', 'Comments', 'Pages'])

print (QA_stuff)


# In[94]:


#Remove hashtag below if you would like an excel file of all relevant content that was pulled
QA_stuff.to_csv(r'C:\Users\cshelton\Desktop\Jupyter_July_QA_Accuracy', index = False)


# In[95]:


#throws out nulls
import numpy as np
QA_stuff[QA_stuff.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]
print(QA_stuff)


# In[96]:


QA_stuff = QA_stuff.astype(float)
QA_stuff


# In[100]:


#Remove hashtag below if you would like an excel file of all relevant content that was pulled
QA_stuff.to_csv(r'C:\Users\cshelton\Desktop\Jupyter_July_QA_Accuracy_4.csv', index = False)


# In[98]:


#additional info if needed
sum_of_errors = QA_stuff["Errors"].sum()
sum_of_pages = QA_stuff["Pages"].sum()
sum_of_comments = QA_stuff["Comments"].sum()
print("The sum of Errors is:", sum_of_errors)
print("The mean of errors is:", QA_stuff["Errors"].mean())
print("The mean of comments is:", QA_stuff["Comments"].mean())
print("The mean of pages is:", QA_stuff["Pages"].mean())
print("The max is:", QA_stuff["Errors"].max())
print("The sum of pages is:",sum_of_pages)
print("The sum of comments is:", sum_of_comments)


# In[101]:


#build accuracy data
n = sum_of_errors
error_per_avg = n/sum_of_pages
print("The total sum of errors is:", QA_stuff["Errors"].sum())
print("The total sum of pages is:", QA_stuff["Pages"].sum())
print("The QA Accuracy rate is:",  1.0 -error_per_avg)


# In[115]:


#locate 5 highest values
top_5_errors = QA_stuff['Errors'].nlargest(5) 
top_5_comments = QA_stuff['Comments'].nlargest(5) 
top_5_pages = QA_stuff['Pages'].nlargest(5) 
print(top_5_errors)
print(top_5_comments)
print(top_5_pages)


# In[ ]:





# In[61]:





# In[ ]:




