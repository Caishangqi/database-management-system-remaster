from lstore.db import Database
from lstore.query import Query
from random import choice, randint, sample, seed
from time import process_time
from lstore.components import *
print("Create database, table, and query demonstration")
records = {}
db = Database()
table_name = str(input("Please choose a name for this table: "))
num_of_columns = int(input("Please choose the number of columns: "))
pk_column = int(input("Please choose which column(index) to become primary key column: "))
print()
table = db.create_table(table_name, num_of_columns, 0)
query = Query(table)
print(table_name + " table created, with " + str(num_of_columns) + " columns, and primary key is in column " + str(pk_column) + "(index)")
print()

print("Insert demonstration")
print("For demonstration reason, the primary key will not be random. The primary key will start with 100 and add 1 for each additional record. Other columns are randomly generated ")
num_of_records = int(input("Please input the number of records that you want to insert: "))
insert_start_time = process_time()
for i in range(0, num_of_records):
    record = []
    for j in range(0, num_of_columns):
        if j == pk_column:
            record.append(100 + i)
        else:
            record.append(randint(0, 5))
    print(record)
    query.insert(*record)
insert_finish_time = process_time()
print("Time took to insert " + str(num_of_records) + " records is " + str(insert_finish_time - insert_start_time) + " seconds.")
print()

print("Select one record demonstration")
select_key = int(input("Please input a key that you want to select: "))
key_index = int(input("Please select the column index that you want to search on: "))
project_column = input("Please select the column(s) that you want to project. \nExample: If you want to project first and second column in a 4 columns total table, please input 1 1 0 0\n")
project_column = project_column.split(" ")
for i in range(0, len(project_column)):
    project_column[i] = int(project_column[i])
result = query.select(select_key, key_index, project_column)
print(result[0].columns)
print()

print("Select mutiple records demonstration")
select_key = int(input("Please input a key that you want to select: "))
key_index = int(input("Please select the column index that you want to search on: "))
project_column = input("Please select the column(s) that you want to project. \nExample: If you want to project first and second column in a 4 columns total table, please input 1 1 0 0\n")
project_column = project_column.split(" ")
result = []
for i in range(0, len(project_column)):
    project_column[i] = int(project_column[i])
result = query.select(select_key, key_index, project_column)
for i in range(0, len(result)):
    print(result[i].columns)
print()


print("Update function demonstration")
update_column = []
for i in range(0, num_of_columns):
    if i == pk_column:
        update_column.append(None)
    else:
        update_column.append(10000)
num_of_records_update = int(input("How many records you want to update: "))
update_start_time = process_time()
for i in range(100, num_of_records_update + 100):
    query.update(i, *update_column)
update_finish_time = process_time()
result = []
project_column = []
for i in range(0, num_of_columns):
    project_column.append(1)

print("Updating " + str(num_of_records_update) + " records:")
for i in range(100, num_of_records_update + 100):
    result = query.select(i, pk_column, project_column)
    # print("From " + str(result[0].columns) + " to " + str(update_column))
print("Time took to update " + str(num_of_records_update) + " records is " + str(update_finish_time - update_start_time) + " second.")

print("Select a record been updated: ")
result = query.select(100, pk_column, project_column)
print(result[0].columns)
print()


print("Sum demonstration")
start_key_range = int(input("Please input the key range that you want to start with: "))
end_key_range = int(input("Please input the key range that you want to end with: "))
sum_column = int(input("Please input the column index that you want to sum: "))
sum_result = query.sum(start_key_range, end_key_range, sum_column)
print(sum_result)
print()




print("Delete demonstration")
num_records_delete = int(input("Please input number of records you want to delete: "))

print("Deleating: ")
for i in range(100, 100 + num_records_delete):
    result = query.select(i, 0, project_column)
    print(result[0].columns)
    query.delete(i)

print("Selecting records been deleted: ")
for i in range(100, 100 + num_records_delete):
    result = []
    result = query.select(i, 0, project_column)
    print("Length of list returned from select function with input (" + str(i) + ", 0, " + str(project_column) + "): " + str(len(result)))





