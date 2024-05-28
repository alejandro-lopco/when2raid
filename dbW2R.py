import configW2R as ini
import mysql.connector as sql
from mysql.connector import Error
import hashlib

CONF = ini.getCnf()
global cnx

def loginDB():
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )
        if cnx is not None:
            return cnx
        else:
            return None
        
    except Error as ErrorConexion:
        print(ErrorConexion)
        return None
    
    finally:        
        try:
            if cnx is not None:
                cnx.close()
        except UnboundLocalError:
            print("Fallo en conexión a la BBDD.")
            return None
    
def checkUser(username):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_limited'],
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
        try:
            if cnx is not None:
                cnx.close()
        except UnboundLocalError:
            print("Fallo en conexión a la BBDD.")
            return None

def checkLogin(username, passwd):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_limited'],
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
        return None
    
    finally:        
        try:
            if cnx is not None:
                cnx.close()
        except UnboundLocalError:
            print("Fallo en conexión a la BBDD.")
        except NameError:
            print("Fallo en conexión a la BBDD.")            

def addUsr(username, passwd, fullName):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_limited'],
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
        try:
            if cnx is not None:
                cnx.close()
        except UnboundLocalError:
            print("Fallo en conexión a la BBDD.")
            return None

def passwdHash(passwd):
    try:
        password_utf = passwd.encode('utf-8')

        sha256hash = hashlib.sha256()
        sha256hash.update(password_utf)

        passwd_hash = sha256hash.hexdigest()

        return passwd_hash
    except:
        print('Error al generar el hash de la contraseña')

def addActividad(
    nombre_actividad,
    descripcion_actividad,
    tipo_actividad,
    privacidad,
    passwd_actividad,
    horas_disponibles
):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
        qryAct  = "INSERT INTO actividades (nombre_actividad,descripcion_actividad,tipo_actividad,privacidad,passwd_actividad) VALUES (%s,%s,%s,%s,%s)"

        cursor.execute(qryAct,(
            nombre_actividad,
            descripcion_actividad,
            tipo_actividad,
            privacidad,
            passwd_actividad,
            horas_disponibles
            ))
        cnx.commit()

        return True
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')

        return False
    
def getTypes():
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
        qryAct  = "SELECT nombre_tipo FROM tipos;"

        cursor.execute(qryAct)

        rslt = cursor.fetchall()

        types = []
        for x in rslt:
            types += x 

        return types
    except Error as ErrorConexion:
        print(f'Error al buscar el tipo: {ErrorConexion}')


        