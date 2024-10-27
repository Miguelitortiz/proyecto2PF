import sqlite3,clase_base,funciones
import pprint


class Alumno(clase_base.Base):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def generar_horario(self) -> list:
        '''
        
Genera y retorna el horario semanal del alumno.

Retorna:
- list: Horario semanal del alumno.

'''
        conexion = sqlite3.connect("prueba4.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Materia WHERE id_alumno = ?", (self.user_id,))
        datos = cursor.fetchall()

        cursor.execute("SELECT nombre FROM Asignaturas")
        asignaturas = cursor.fetchall()

        horario = [[None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None, None]]

        for dato in datos:
            for i in range(1, 6):
                for j in range(1, 10):
                    if dato[-2] == i and dato[-1] == j:
                        horario[i-1][j-1] = asignaturas[dato[1]-1]
                        break

        conexion.commit()
        conexion.close()

        return horario

    def generar_horario_dia(self, dia:int) -> list:
        '''
        
Genera el horario del alumno para un día específico.

Parámetros:
- dia (int): Día de la semana (1 a 5).

Retorna:
- list: Horario del día especificado.

'''
        conexion = sqlite3.connect("prueba4.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Materia WHERE id_alumno = ? AND id_dia = ?", (self.user_id, dia))
        datos = cursor.fetchall()

        cursor.execute("SELECT nombre FROM Asignaturas")
        asignaturas = cursor.fetchall()

        horario = [None, None, None, None, None, None, None, None, None]

        for dato in datos:
            for j in range(1, 10):
                if dato[-1] == j:
                    horario[j-1] = asignaturas[dato[1]-1]
                    break

        conexion.commit()
        conexion.close()

        return horario

    def modificar_asistencia(self, id_clase: int, dia: int, mes: int, año: int, asistencia: bool) -> bool:
        '''
Modifica el estado de asistencia para el alumno en una clase específica.

Parámetros:
- id_clase (int): ID de la clase.
- dia (int): Día.
- mes (int): Mes.
- año (int): Año.
- asistencia (bool): Estado de asistencia.

Retorna:
- bool: True si se actualizó la asistencia, False en caso contrario.
'''
        
        conexion = sqlite3.connect("prueba4.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Registro WHERE dia = ? AND id_mes = ? AND año = ? AND id_materia = ? AND asistencia = ?",
                       (dia, mes, año, id_clase, asistencia))
        datos = cursor.fetchall()
        if datos:
            cursor.execute("INSERT INTO Registro (dia, id_mes, año, id_materia, asistencia) VALUES (?, ?, ?, ?, ?)",
                           (dia, mes, año, id_clase, asistencia))
        else:
            cursor.execute("UPDATE Registro SET asistencia = ? WHERE dia = ? AND id_mes = ? AND año = ? AND id_materia = ?",
                           (asistencia, dia, mes, año, id_clase))
            conexion.commit()
            conexion.close()
            return True
        
    
    
    
if __name__ == "__main__":
    num,Moi = funciones.login(20206554,'Miguel05')
    horario = Moi.generar_horario()
    pprint.pprint(horario)
   