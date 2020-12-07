import sqlite3
def read_from_police_officer_db():
    cases_dict=dict()
    conn=sqlite3.connect('policeofficer.db')
    c=conn.cursor()
    c.execute('SELECT * FROM cases')
    data = c.fetchall()
    #print(data)
    
    for row in data:
        cases_dict[str(row[0])]=row[1]
        #print(row)
    c.close()
    conn.close()
    return cases_dict
print(read_from_db())
