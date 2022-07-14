# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 20:41:22 2022

@author: Jacqueline Kelly
"""
import psycopg2
import os
from dotenv import load_dotenv

# getting environmental variables to access db
load_dotenv()

#establishing the connection
conn = psycopg2.connect(
   database=os.getenv('database'), 
   user=os.getenv('user'),
   password=os.getenv('password'), 
   host=os.getenv('dbhost'), 
   port=os.getenv('port')
)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

conn.commit()
conn.close()
