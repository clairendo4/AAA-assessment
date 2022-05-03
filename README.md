# AAA-assessment

**Detailed instructions on of How to run your program - Including how to set up the sql lite database
connection**
- For this project, I used Jupyter notebook so an easy way to run this program , is to use jupyter notebook or google colab
- First, make sure python version 3 and above is installed .
- we need to install all  modules needed for this task. install simple_salesforce using pip  and 
as for pandas, you can install that as well if using another IDE other than Jupyter notebook
- import libraries ( import pandas,from pandas... import DataFrame,and import salesforce from simple_salesforce)
- create a connection to the salesforce API - best practice is to avoid hard coding credentials into your script, import salesforce login 
for that and load credentials from a json file, code available and commented out

Setting up SQLITE connection
- first, import sqlite3
- use connect() function to create a connection object and a cursor 
- SQLITE can automatically create a db file in the current working directory for you if you do not have one already

**Output summary of what you built that includes - the number of objects, fields per object and # of
fields and their datatypes e.g. The result should be -**
last part of code
**What are some of the design considerations you chose to include in your code, what impact does it
have on the objects you created?**
i included batch size fetch method into my script because i noticed pulling the metadata from salesforce comes in batches so i made sure
my function continues after loading the first batch of records
**How would you scale your program if the number of salesforce objects scaled to thousands and
millions?**
I can overcome this by using the salesforce bulk API
**How would you dynamically modify your table structure to account for changes to your metadata. i.e a
new column is added to account table or zipcode changes from int to varchar**

i will modify my program with a while loop to look at schema of data and append if new column or update datatype based on the changes
