import configW2R as ini
import mysql.connector 
from mysql.connector import Error

conf = ini.getCnf()

def loginDB():
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usuario_final',
            password='Final_User'
        )
        if cnx.is_connected():
            return cnx
        else:
            return None
    
    except Error as ErrorConexion:
        print(ErrorConexion)
        return None
    
def checkUser(username):
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password='creador_usuario'
        )
        if cnx.is_connected():
            cursor = cnx.cursor()

            query = "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s;"
            cursor.execute(query,(username))

            rslt = cursor.fetchone()

            if rslt[0] > 0:
                return True
            else:
                return False

    except Error as ErrorConexion:
        print(ErrorConexion)
        return False
    
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close() 

def checkLogin(username, passwd):
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password='creador_usuario'
        )
        if cnx.is_connected():
            cursor = cnx.cursor()

            query = "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s AND passwd_usuario = %s;"
            cursor.execute(query,(username,passwd))

            rslt = cursor.fetchone()

            if rslt[0] > 0:
                return True
            else:
                return False

    except Error as ErrorConexion:
        print(ErrorConexion)
        return False
    
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()

def addUsr(username, passwd, fullName):
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password='creador_usuario'
        )
        if cnx.is_connected():
            cursor = cnx.cursor()
            query = "INSERT INTO usuarios (nombre_usuario,passwd_usuario,nombre_completo) VALUES (%s,%s,%s);"
            cursor.execute(query,(username,passwd,fullName))

    except Error as ErrorConexion:
        print(ErrorConexion)
        return False

    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
