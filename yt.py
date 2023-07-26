import pymysql
import pandas as pd
import sqlalchemy as sa 

# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     #password='password',
#     db='test',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )

#create sqlalchemy engine

add = True
engine = sa.create_engine("mysql+pymysql://root:@localhost/test")
                   
if add:
    yt = pd.read_excel('yt.xlsx')
    yt.index.name = 'id'
    yt.to_sql('time', con = engine, if_exists = 'append', chunksize = 1000, index=False)

#stmt = sa.select([time])

#stmt = sa.select(time').where('time'.c.name == "Pesach")
sql = "select * From time"
df = pd.read_sql(sql,con=engine)

# with engine.connect() as conn:
#      for row in conn.execute(stmt):
#         print(row)

print(df)

# try:
#     with conn.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `time` (`date`, `name`, `recipients`) VALUES (%s, %s, %s)"
#         cursor.execute(sql, ('9 Av', "T B'Av", 'All'))

#     # Commit changes
#     conn.commit()

#     print("Record inserted successfully")
# finally:
#     conn.close()

# try:
#     with conn.cursor() as cursor:
#         # Read data from database
#         sql = "SELECT * FROM `time`"
#         cursor.execute(sql)

#         # Fetch all rows
#         rows = cursor.fetchall()

#         # Print results
#         for row in rows:
#             print(row)
# finally:
#     conn.close()