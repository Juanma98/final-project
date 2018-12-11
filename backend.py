import sqlite3
def connect():
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS calendar (id INTEGER PRIMARY KEY, patient text, doctor text, dates integer, code_illness text, drug text, telefone integer)")
    conn.commit()
    conn.close()

def insert(patient,doctor,dates,code_illness,drug,telefone):
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO calendar VALUES (NULL,?,?,?,?,?,?)",(patient,doctor,dates,code_illness,drug,telefone))
    conn.commit()
    conn.close()
    view()
def registered(patient,telefone,date,doctor):
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO calendar VALUES (NULL,?,?,?,NULL,NULL,?)",(patient,doctor,date,telefone))
    conn.commit()
    conn.close()
    view()

def view():
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM calendar")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(patient="",doctor="",dates="",code_illness="",drug="",telefone=""):
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM calendar WHERE patient=? OR doctor=? OR dates=? OR code_illness=? OR drug=? OR telefone=?", (patient,doctor,dates,code_illness,drug,telefone))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM calendar WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update(id,patient,doctor,dates,code_illness,drug,telefone):
    conn=sqlite3.connect("calendar.db")
    cur=conn.cursor()
    cur.execute("UPDATE calendar SET patient=?, doctor=?, dates=?, code_illness=?, drug=?, telefone=? WHERE id=? ",(patient,doctor,dates,code_illness,drug,telefone,id))
    conn.commit()
    conn.close()

connect()
#insert("David Viar","Dr. Parker",15062018,"EWFASF","SDFASFF")
#delete()
#update(4,"The moon","John Smooth",1917,99999)
#print(view())
#print(search(doctor="John Smith"))
