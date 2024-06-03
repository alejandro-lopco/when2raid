import configW2R as ini
import mysql.connector as sql
from mysql.connector import Error
import hashlib
import datetime

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

        ID_USER = CONF['USER']['default']

        qryAct  = "INSERT INTO actividades (nombre_actividad,descripcion_actividad,tipo_actividad,passwd_actividad,fecha,autor) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(qryAct,(
            nombre_actividad,
            descripcion_actividad,
            tipo_actividad,
            passwd_actividad,
            fecha,
            ID_USER))

        ID_ACT  = cursor.lastrowid
        
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
    
def getHorasDisponibles(act,user):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
        qryAct  = "SELECT hora_inicio,hora_final FROM horas_disponibles WHERE id_actividad = (%s) AND id_usuario = (%s);"

        cursor.execute(qryAct,(act,user))

        rslt = cursor.fetchone()

        if rslt is not None:
            horaInicio  = timeDeltaHoras(rslt[0])
            horaFinal   = timeDeltaHoras(rslt[1])

            horasAct = [horaInicio,horaFinal]
        else:
            return None
        
        return horasAct
    except Error as ErrorConexion:
        print(f'Error al buscar el tipo: {ErrorConexion}')
        cnx.rollback()

def getAllHorasDisponibles(act):
    try:
        if isinstance(act, int):
            idAct = act
        elif isinstance(act, (list, tuple)) and len(act) > 0:
            idAct = act[0]
        else:
            raise ValueError(f"Valor no esperado (qué haces tio.): {act}")          
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor      = cnx.cursor()
        qryHoras    = "SELECT id_usuario,hora_inicio,hora_final FROM horas_disponibles WHERE id_actividad = %s;"

        cursor.execute(qryHoras,(idAct,))

        rslt = cursor.fetchall()
        listaHoras = []
        for x in rslt:
            horaUnica = []
            horaUnica.append(x[0])
            horaUnica.append(timeDeltaHoras(x[1]))
            horaUnica.append(timeDeltaHoras(x[2]))
            listaHoras.append(horaUnica)

        cnx.commit()

        return listaHoras
    except Error as ErrorConexion:
        print(f'Error al buscar el tipo: {ErrorConexion}')
        cnx.rollback()

def timeDeltaHoras(timeDelta):
    SEGUNDOS    = int(timeDelta.total_seconds())

    HORAS       = SEGUNDOS // 3600
    MINUTOS     = (SEGUNDOS % 3600) // 60

    formatHoras = f"{HORAS:02}:{MINUTOS:02}"
    return formatHoras
    
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

        cnx.commit()

        if rslt is not None:
            return rslt[0]
        else: 
            return None
    
    except Error as ErrorConexion:
        print(f'Error al buscar el tipo: {ErrorConexion}')    
        cnx.rollback()

def getTypeName(id):
    try:
        # Nos conectamos a la base de datos
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()
        qryAct  = "SELECT nombre_tipo FROM tipos WHERE id_tipo = %s;"

        cursor.execute(qryAct,(id,))

        rslt = cursor.fetchone()

        cnx.commit()

        return rslt[0]
    
    except Error as ErrorConexion:
        print(f'Error al buscar el nombre: {ErrorConexion}')    
        cnx.rollback()

def dateSQLFormat(fecha):
    ANYO    = fecha[2]
    MES     = fecha[0]
    DIA     = fecha[1]

    fechaSQL = f"{ANYO:04d}-{MES:02d}-{DIA:02d}"
    return fechaSQL    

def timeSQLFormat(hora, min):
    horaMysql = str(f'{int(hora):02d}:{int(min):02d}:00')

    return horaMysql

def getApuntadas(user):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )
        cursor = cnx.cursor()

        qry = 'SELECT * FROM horas_disponibles WHERE id_usuario = %s;'
        cursor.execute(qry,(user,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Ha ocurrido un error al buscar las actividades: {ErrorConexion}')
        cnx.rollback()
        return None

def getActInfo(id):
    try:
        if isinstance(id, int):
            idAct = id
        elif isinstance(id, (list, tuple)) and len(id) > 0:
            idAct = id[0]
        else:
            raise ValueError(f"Valor no esperado (qué haces tio.): {id}")  
                 
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )
        cursor = cnx.cursor()

        qry = 'SELECT * FROM actividades WHERE id_actividad = %s'
        cursor.execute(qry,(idAct,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Ha ocurrido un error al buscar las actividades: {ErrorConexion}')
        cnx.rollback()
        return None
    
def autorAct(actId):
    UPDT_CONF = ini.getCnf()
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )
        cursor = cnx.cursor()

        qry = 'SELECT autor FROM actividades WHERE id_actividad = %s'
        cursor.execute(qry,(actId,))

        rslt = cursor.fetchone()

        cnx.commit()

        if rslt[0] == UPDT_CONF['USER']['default']:
            return True
        else:
            return False
    except Error as ErrorConexion:
        print(f'Ha ocurrido un error al buscar las actividades: {ErrorConexion}')
        cnx.rollback()
        return None
    
def horaMin():
    HORAS   = [x for x in range(0,24)]
    MINUTOS = [y for y in range(0,60)]

    return HORAS,MINUTOS

def updateActividad(
    id_act,
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

        ID_USER = CONF['USER']['default']

        qryAct  = "UPDATE actividades SET nombre_actividad = %s, descripcion_actividad = %s, tipo_actividad = %s, passwd_actividad = %s, fecha = %s WHERE id_actividad = %s AND autor = %s"
        cursor.execute(qryAct,(
            nombre_actividad,
            descripcion_actividad,
            tipo_actividad,
            passwd_actividad,
            fecha,
            id_act,
            ID_USER))
        
        cnx.commit()

        try:
            updateHorasDisponibles(
                id_act,
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

def updateHorasDisponibles(
    actID,
    user,
    horaInicio,
    horaFinal      
):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor(buffered=True)

        qryHoras    = "SELECT id_usuario,hora_inicio,hora_final FROM horas_disponibles WHERE id_actividad = %s AND id_usuario = %s;"
        rslt = cursor.execute(qryHoras,(actID,user))
        
        if rslt is None:
            qryNewHoras = 'INSERT INTO horas_disponibles (id_actividad,id_usuario,hora_inicio,hora_final) VALUES (%s,%s,%s,%s)'
            cursor.execute(qryNewHoras,(actID,user,horaInicio,horaFinal))
        else:
            qryNewHoras = 'UPDATE horas_disponibles SET hora_inicio = %s, hora_final = %s WHERE id_actividad = %s AND id_usuario = %s'
            cursor.execute(qryNewHoras,(horaInicio,horaFinal,actID,user))

        cnx.commit()

        return True
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

    
def deleteAct(actID):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qryDropHoras = 'DELETE FROM horas_disponibles WHERE id_actividad = %s'
        cursor.execute(qryDropHoras,(actID,))        

        qryDropAct = 'DELETE FROM actividades WHERE id_actividad = %s'
        cursor.execute(qryDropAct,(actID,))

        cnx.commit()

        return True
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False
    
def delHoras(actID,user):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qryDropHoras = 'DELETE FROM horas_disponibles WHERE id_actividad = %s AND id_usuario = %s'
        cursor.execute(qryDropHoras,(actID,user))        

        cnx.commit()

        return True
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False
    
def formatActSelect(actividades):
    misActividades      = []

    for x in actividades:
        actInfo = getActInfo(x[0])
        listaInfo = [list(y) for y in actInfo]

        if listaInfo[0][4] is not None:
            listaInfo[0][4] = True
        else:
            listaInfo[0][4] = False

        listaInfo[0][3] = getTypeName(listaInfo[0][3])

        misActividades += listaInfo

    return misActividades

def nameSearch(name):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT * FROM actividades WHERE nombre_actividad = %s'
        cursor.execute(qrySearch,(name,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

def authorSearch(autor):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT * FROM actividades WHERE autor = %s'
        cursor.execute(qrySearch,(autor,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

def typeSearch(typeName):
    try:
        typeID = getTypeID(typeName)

        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT * FROM actividades WHERE tipo_actividad = %s'
        cursor.execute(qrySearch,(typeID,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

def privateSearch(typeName):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT * FROM actividades WHERE passwd_actividad != NULL;'
        cursor.execute(qrySearch)

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False

def dateSearch(date):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT * FROM actividades WHERE fecha = %s;'
        cursor.execute(qrySearch,(date,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False
    
def getTypeInfo(typeName):
    try:
        cnx = sql.connect(
            host    =CONF['DATABASE']['hostname'],
            database=CONF['DATABASE']['db_name'],
            user    =CONF['DATABASE']['db_user'],
            password=''
        )

        cursor  = cnx.cursor()

        qrySearch = 'SELECT nombre_tipo,desc_tipo FROM tipos WHERE nombre_tipo = %s;'
        cursor.execute(qrySearch,(typeName,))

        rslt = cursor.fetchall()

        cnx.commit()

        return rslt
    except Error as ErrorConexion:
        print(f'Error al generar la actividad: {ErrorConexion}')
        cnx.rollback()
        return False
