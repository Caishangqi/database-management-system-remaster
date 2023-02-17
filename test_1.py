from lstore.db import Database
from lstore.query import Query
from random import choice, randint, sample, seed
from time import process_time
from lstore.components import Record


db = Database()
tb = db.create_table("Test", 4, 1)
query = Query(tb)
# Insert
for i in range (0, 20):
    tmp = []
    for j in range(0, 4):
        if j == 1:
            tmp.append(1000 + i)
        else:
            tmp.append(randint(0, 5))
    print(tmp)
    query.insert(*tmp)
print()



# Select
# Select one record
# result = query.select(1000, 0, [1, 1, 1, 1])
# print(result[0].columns)
# print()

result = []

#Select mutiple records
# result = query.select(1, 1, [1, 1, 1, 1])
# for i in range(0, len(result)):
#     print(result[i].columns)
# print()



# Delete
# query.delete(1007)
# result = query.select(1007, 0, [1, 1, 1, 1])
# if len(result) == 0:
#     print("Delete successful")
# print()

print()
# Update
update_column = [100, None, 100, 100]
for i in range(1000, 1003):
    query.update(i, *update_column)
result = []
result = query.select(100, 0, [1, 1, 1, 1])
print(result[0].columns)



# Sum
# sum_result = query.sum(1000, 1005, 2)
# print(sum_result)