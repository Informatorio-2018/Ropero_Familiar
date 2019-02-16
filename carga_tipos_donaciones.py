import sqlite3

# establecer la concexión
conexion = sqlite3.connect("db.sqlite3")

# crear un cursor para realizar la consulta
consulta = conexion.cursor()

# insertar datos en tabla Tipos de Donaciones
reg1 = ("Ropa", "kg", 0)
reg2 = ("Calzados", "par", 0)
reg3 = ("Accesorios", "un", 0)
reg4 = ("Otros", "un", 0)

sql = "INSERT INTO donaciones_typesdonation(name, unit_measure, quantity_total) VALUES(?, ?, ?)"
error = False

try:
    consulta.execute(sql, reg1)
    consulta.execute(sql, reg2)
    consulta.execute(sql, reg3)
    consulta.execute(sql, reg4)
except:
	error = True
	conexion.rollback()

if not error:
    conexion.commit()
    print("Tipos de donaciones registrados!")
    input()
else:
    conexion.rollback()
    print("No se pudieron registrar los tipos de donaciones!")
    input()


consulta.close()
conexion.close()
