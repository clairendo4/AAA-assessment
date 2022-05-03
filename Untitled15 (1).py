#!/usr/bin/env python
# coding: utf-8

# In[236]:


#installing simple-salesforce
get_ipython().system('pip install simple-salesforce')


# In[234]:


#importing libraries
import json
import pandas as pd
from pandas import DataFrame
from simple_salesforce import Salesforce, SalesforceLogin, SFType
loginCredentials = json.load(open('Login.json'))

#connecting to salesforce API using my credentials, you can also call a json file as below to avoid hard coding credentials
# username =loginCredentials['username']
# password = loginCredentials['password']
# security_token = loginCredentials['token']
# domain = 'login'
# session_id, instance = SalesforceLogin(username=username, password = password, security_token = token)
# sf = Salesforce(instance=instance, session_id=session_id)



sf = Salesforce(username='ndoforbih@yahoo.com', password='2Dec.lairen', security_token='pq5Qm8qsm7v6Zxxr36XNzRLLR')


# In[115]:


#TESTING CONNECTION
print(sf)


# In[294]:


#taking a glance at my metadata
metadata_org = sf.describe()
#creating a dataframe of my sobjects for a better view
df = pd.DataFrame(metadata_org['sobjects'])
print(df)


# In[132]:


#converting accounts fields into a dataframe
account = sf.account
df_accounts_fields = pd.DataFrame(accounts_metadata.get('fields'))
print(df_accounts_fields)


# In[258]:


# creating sqlite3 connection
import sqlite3
conn = sqlite3.connect('sqlitedb')  #this sqlite db file will be created in my directory

# populating a new database in sqlite with metadata from accounts object
df = df.applymap(str)
df.to_sql(name='salesforce_account', con=conn, if_exists = 'replace' ) #creates a table with name salesforce_account
pd.read_sql('select * from salesforce_account', conn) #loads table with all fields


# In[296]:


#defining a function to pull the metadata from salesforce API in batches

def SOQL(SOQL):
    qryResult = sf.query(SOQL)
#     print('Record count{0}'.format(qryResult['totalsize']))
    
    isDone = qryResult['done'];
    
    if isDone == True:
        df1 = DataFrame(qryResult['records'])
    while isDone != True:
        try:
            if qryResult['done'] != True:
                df1 = df.append(DataFrame(qryResult['records']));
                qryResult = sf.query_more(qryResult['nextRecordsUrl'], True)
            else:
                df1 = df.append(DataFrame(qryResult['records']))
                isDone = True;
                print('completed')
                break;
        except NameError:
            df1 = DataFrame(qryResult['records'])
            qry = sf.query_more(qryResult['nextRecords'], True)
   
    return df1;


# In[256]:


SOQL('SELECT id, Name FROM Opportunity LIMIT 5')


# In[254]:


SOQL("SELECT id, ContactEmail, IsEscalated FROM Case LIMIT 5")


# In[300]:


# CODE TO GENERATE SQL STATEMENTS

SOURCE = df
TARGET = 'salesforceTBL'
cur = conn.cursor()

def GENERATE_SQL(SOURCE, TARGET):

# SQL_CREATE_STATEMENT_FROM_DATAFRAME(SOURCE, TARGET)
   
    sql_text = pd.io.sql.get_schema(SOURCE, TARGET)   
    print(sql_text)
GENERATE_SQL(SOURCE, TARGET)     


# In[223]:


# CODE TO GENERATE INSERT SQL STATEMENTS
import re 
import pandas as pd 

table = 'salesforce_account'


df = pd.read_sql_query(f'select * from {table}', con=conn)


cols = ', '.join(df.columns.to_list()) 
vals = []

for index, r in df.iterrows():
    row = []
    for x in r:
        row.append(f"'{str(x)}'")

    row_str = ', '.join(row)
    vals.append(row_str)

f_values = [] 
for v in vals:
    f_values.append(f'({v})')

# Handle inputting NULL values
f_values = ', '.join(f_values) 
f_values = re.sub(r"('None')", "NULL", f_values)

sql = f"insert into {table} ({cols}) values {f_values};" 

print(sql)


db.dispose()


# In[311]:


# SUMMARY OF THE TABLES BUILD
pd.read_sql('select count(*) from salesforce_account', conn)


# In[ ]:




