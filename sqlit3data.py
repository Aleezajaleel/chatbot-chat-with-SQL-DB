# We will create sqlite3 datbase locally
# we will inside some initial data (like student table)
# confirm that the table is created and the rows are inserted.
# Prepare the DB wo we cn later query it with langchain

import sqlite3

# create a student.db with a student table

# connect to (or create) aa local SQLite DB file
connection = sqlite3.connect("student.db")

# create a cursor object to insert record, create table
cursor = connection.cursor()

# now I will define a SQL statement to create aa table (if not exist)

table_info = '''
create table STUDENT( 
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INTEGER 
    );
'''
# this execution with create STUDENT table
cursor.execute(table_info)

# We will be inserting some sample records

cursor.execute("INSERT INTO STUDENT VALUES('Malik95','Data Science','A',95)")
cursor.execute("INSERT INTO STUDENT VALUES('Ali','Data Science','B',88)")
cursor.execute("INSERT INTO STUDENT VALUES('Charlie','Data Science','A',72)")
cursor.execute("INSERT INTO STUDENT VALUES('Diana','Data Science','C',64)")
cursor.execute("INSERT INTO STUDENT VALUES('Ethan','Data Science','A',91)")

cursor.execute("INSERT INTO STUDENT VALUES('Fiona','DevOps','A',78)")
cursor.execute("INSERT INTO STUDENT VALUES('George','DevOps','B',83)")
cursor.execute("INSERT INTO STUDENT VALUES('Hannah','DevOps','A',99)")
cursor.execute("INSERT INTO STUDENT VALUES('Ian','DevOps','C',56)")
cursor.execute("INSERT INTO STUDENT VALUES('Jade','DevOps','B',81)")

cursor.execute("INSERT INTO STUDENT VALUES('Kevin','Marketing','A',92)")
cursor.execute("INSERT INTO STUDENT VALUES('Laura','Marketing','B',70)")
cursor.execute("INSERT INTO STUDENT VALUES('Martin','Marketing','C',66)")
cursor.execute("INSERT INTO STUDENT VALUES('Nina','Marketing','A',89)")
cursor.execute("INSERT INTO STUDENT VALUES('Oscar','Marketing','B',73)")

cursor.execute("INSERT INTO STUDENT VALUES('Paula','Sales','C',58)")
cursor.execute("INSERT INTO STUDENT VALUES('Quentin','Sales','B',79)")
cursor.execute("INSERT INTO STUDENT VALUES('Rebecca','Sales','A',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Sam','Sales','B',67)")
cursor.execute("INSERT INTO STUDENT VALUES('Tara','Sales','C',54)")

cursor.execute("INSERT INTO STUDENT VALUES('Uma','Finance','A',88)")
cursor.execute("INSERT INTO STUDENT VALUES('Victor','Finance','A',93)")
cursor.execute("INSERT INTO STUDENT VALUES('Wendy','Finance','C',62)")
cursor.execute("INSERT INTO STUDENT VALUES('Xavier','Finance','B',77)")
cursor.execute("INSERT INTO STUDENT VALUES('Yvonne','Finance','A',100)")

cursor.execute("INSERT INTO STUDENT VALUES('Zack','HR','C',48)")
cursor.execute("INSERT INTO STUDENT VALUES('Abel','HR','B',69)")
cursor.execute("INSERT INTO STUDENT VALUES('Bianca','HR','A',87)")
cursor.execute("INSERT INTO STUDENT VALUES('Caleb','HR','A',95)")
cursor.execute("INSERT INTO STUDENT VALUES('Denise','HR','C',60)")

cursor.execute("INSERT INTO STUDENT VALUES('Ernest','IT','B',84)")
cursor.execute("INSERT INTO STUDENT VALUES('Fatima','IT','A',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Gina','IT','B',75)")
cursor.execute("INSERT INTO STUDENT VALUES('Harvey','IT','C',53)")
cursor.execute("INSERT INTO STUDENT VALUES('Iris','IT','A',99)")

cursor.execute("INSERT INTO STUDENT VALUES('Jonas','Management','B',76)")
cursor.execute("INSERT INTO STUDENT VALUES('Kylie','Management','C',65)")
cursor.execute("INSERT INTO STUDENT VALUES('Leon','Management','A',92)")
cursor.execute("INSERT INTO STUDENT VALUES('Macy','Management','B',80)")
cursor.execute("INSERT INTO STUDENT VALUES('Nick','Management','C',55)")

cursor.execute("INSERT INTO STUDENT VALUES('Olivia','Operations','A',85)")
cursor.execute("INSERT INTO STUDENT VALUES('Pavel','Operations','B',72)")
cursor.execute("INSERT INTO STUDENT VALUES('Rita','Operations','C',61)")
cursor.execute("INSERT INTO STUDENT VALUES('Soren','Operations','A',96)")
cursor.execute("INSERT INTO STUDENT VALUES('Tessa','Operations','B',86)")

cursor.execute("INSERT INTO STUDENT VALUES('Ulysses','Support','C',59)")
cursor.execute("INSERT INTO STUDENT VALUES('Vera','Support','A',94)")
cursor.execute("INSERT INTO STUDENT VALUES('Walter','Support','B',68)")
cursor.execute("INSERT INTO STUDENT VALUES('Ximena','Support','A',97)")
cursor.execute("INSERT INTO STUDENT VALUES('Yuri','Support','C',63)")

## commit chanages so they persist
connection.commit()

# (Optional) Print out inserted records to confirm 
# It will display all records

print("Inserted Records:")
data = cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

## committed chaanges now closing the connection.
connection.close()