#to handle dataabase connection

import psycopg2
from psycopg2.extras import RealDictCursor
import time

def get_db():
 while True:
   try:
     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Learning@tools1', cursor_factory=RealDictCursor) #connect to the databaseclea
     cursor = conn.cursor()  #create a cursor to execute SQL queries
     print("Database connection successful")
     break  #break the loop if connection is successful
   except Exception as error:
     print("Database connection failed")
     print("Error:", error)
     time.sleep(2)  #wait for 2 seconds before trying to connect again


 try:
    yield conn
 finally:
   conn.close()