import sqlite3
import time
import os
from zipfile import ZipFile
def create_zip(folder_path):
    zipObj = ZipFile('sample.zip', 'w')
    for filename in os.listdir(folder_path):
        print(os.path.join(folder_path, filename))
        zipObj.write(os.path.join(folder_path, filename))
    # close the Zip File
    zipObj.close()
def read_from_database():
    conn=sqlite3.connect('acc')
    c=conn.cursor()
    c.execute('SELECT * FROM cement_bags')
    data = c.fetchall()
    for row in data:
        print(row)
    c.close()
    conn.close()
    return data
def write_to_database(time_stamp,warehouse_location,stack_number,stack_bag_count,stack_location):
    conn = sqlite3.connect('acc')
    c = conn.cursor()
    c.execute("INSERT INTO cement_bags(time_stamp, warehouse_location, stack_number, stack_bag_count,stack_location) VALUES (?, ?, ?, ?, ?)",
          (time_stamp, warehouse_location, stack_number, stack_bag_count,stack_location))
    conn.commit()
    c.close()
    conn.close()
time_stamp=time.time()
#write_to_register(time_stamp,'Chembur',1,35,'yash/Downloads/images')
create_zip('sample_images_test')
