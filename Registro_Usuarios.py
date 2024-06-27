import sqlite3
from datetime import datetime

conn = sqlite3.connect('Database Ventas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Match_Ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                edad INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                producto TEXT NOT NULL)''')



def registrar_comprador():
    nombre = input("Nombre: ")
    email = input("Email: ")
    edad = int(input("Edad: "))
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    producto = input("Producto comprado: ")

    c.execute('INSERT INTO Match_Ventas (nombre, email, edad, fecha, producto) VALUES (?, ?, ?, ?, ?)',
              (nombre, email, edad, fecha, producto))
    conn.commit()
    print("Comprador registrado exitosamente!")



registrar_comprador()


conn.close()
