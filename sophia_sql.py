from platform import mac_ver
import pyodbc


#MySql Connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=TaanyBaza;UID=sa;PWD=Taanydominira123')
cursor = conn.cursor()


#SQL MAC ADRESS
def get_mac():
    cursor.execute("SELECT count(*) as tot FROM MacAdresa")
    data = cursor.fetchone()[0]
    return data 

def insert_mac(mac_adress,MyText):
    cursor.execute("INSERT INTO MacAdresa (mac, ime) VALUES(?,?)", str(mac_adress), str(MyText))
    cursor.commit()

def get_name():
    cursor.execute("SELECT ime FROM MacAdresa")
    name = cursor.fetchall()
    return name