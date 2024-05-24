import configW2R as ini
import mysql.connector 
from mysql.connector import Error
import hashlib

conf = ini.getCnf()

def loginDB():
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usuario_final',
            password=''
        )
        if cnx is not None:
            return cnx
        else:
            return None
    
    except Error as ErrorConexion:
        print(ErrorConexion)
        return None
    
def checkUser(username):
    try:
        global cnx
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password=''
        )
        if cnx is not None:
            cursor = cnx.cursor()

            query = "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s;"
            cursor.execute(query,(username,))

            rslt = cursor.fetchone()

            if rslt[0] > 0:
                return True
            else:
                return False

    except Error as ErrorConexion:
        print(ErrorConexion)
        return None
    
    finally:
        if cnx is not None:
            cursor.close()
            cnx.close() 

def checkLogin(username, passwd):
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password=''
        )
        if cnx is not None:
            cursor = cnx.cursor()

            query = "SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s AND passwd_usuario = %s;"
            cursor.execute(query,(username,passwd,))

            rslt = cursor.fetchone()

            if rslt[0] > 0:
                return True
            else:
                return False

    except Error as ErrorConexion:
        print(ErrorConexion)
        return False
    
    finally:
        if cnx is not None:
            cursor.close()
            cnx.close()

def addUsr(username, passwd, fullName):
    try:
        # Nos conectamos a la base de datos
        cnx = mysql.connector.connect(
            host    =conf['DATABASE']['hostname'],
            database='when2raid',
            user    ='usario_limitado',
            password=''
        )
        if cnx is not None:
            cursor = cnx.cursor()
            query = "INSERT INTO usuarios VALUES (%s,%s,%s);"

            cursor.execute(query,(username,passwd,fullName))

            cnx.commit()

            return True 

    except Error as ErrorConexion:
        print(ErrorConexion)
        return False

    finally:
        if cnx is not None:
            cursor.close()
            cnx.close()

def passwdHash(passwd):
    try:
        password_utf = passwd.encode('utf-8')

        sha256hash = hashlib.sha256()
        sha256hash.update(password_utf)

        passwd_hash = sha256hash.hexdigest()

        return passwd_hash
    except:
        pass