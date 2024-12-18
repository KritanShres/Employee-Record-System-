import mysql.connector 

database = mysql.connector.connect(
    host= 'localhost', 
    user = 'root', 
    password = 'kritan69420'
)


cursorObject = database.cursor() 

cursorObject.execute("CREATE DATABASE kritan")

print("all done") 