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
    passwd_actividad,
    fecha,
    horaInicio,
    horaFinal
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

        qryAct  = "INSERT INTO actividades (nombre_actividad,descripcion_actividad,tipo_actividad,passwd_actividad,fecha) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(qryAct,(
            nombre_actividad,
            descripcion_actividad,
            tipo_actividad,
            passwd_actividad,
            fecha))

        ID_ACT  = cursor.lastrowid
        ID_USER = CONF['USER']['default']

        
        cnx.commit()

        try:
            addHorasDisponibles(
                ID_ACT,
                ID_USER,
                horaInicio,
                horaFinal
            )

            return True
        except Error as ErrorConexion:
            cnx.rollback()
            return False
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

def addHorasDisponibles(idAct,idUser,horaInicio,horaFinal):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
                
        qryTime = 'INSERT INTO horas_disponibles VALUES (%s,%s,%s,%s);'
        cursor.execute(qryTime,(
            idAct,
            idUser,
            horaInicio,
            horaFinal))
        
        cnx.commit()

        return True
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
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
        cnx.rollback()

def getTypeID(typeName):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
        qryAct  = "SELECT id_tipo FROM tipos WHERE nombre_tipo = %s;"

        cursor.execute(qryAct,(typeName,))

        rslt = cursor.fetchone()
        return rslt[0]
    
    except Error as ErrorConexion:
        print(f'Error al buscar el tipo: {ErrorConexion}')    

def dateSQLFormat(fecha):
    ANYO    = fecha[2]
    MES     = fecha[0]
    DIA     = fecha[1]

    fechaSQL = f"{ANYO:04d}-{MES:02d}-{DIA:02d}"
    return fechaSQL

def timeSQLFormat(hora, min):
    horaMysql = str(f'{hora:02d}:{min:02d}:00')

    return horaMysql