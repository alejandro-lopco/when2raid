import PySimpleGUI as sg
import loginW2R as lg
import dbW2R as db
import configW2R as cnf
import datetime
from PIL import Image                    


def setupMainGUI():
    sg.theme(cnf.getTheme())

    # Definición de opciones en la toolbar
    MENU_DEF = [
        ['&Aplicación',['&Salir','&Cerrar Sesión']],
        ['&Actividades',['&Crear Actividad']] 
    ]

    HEADER = [
        'ID',
        'Nombre',
        'Descripción',
        'Pelea',
        'Privada',
        'Fecha',
        'Autor'
    ]

    HOME_DEF = [
        [sg.Text(f'Bienvenido {CONFIG['USER']['default']}',
                 font=('Arial bold',22),
                 pad=(50,10),
                 expand_x=True)],
        [sg.Text('Tus actividades:'),
         sg.Button('Editar',
                   expand_x=True,
                   border_width=(5)),
         sg.Button('Borrar',
                   expand_x=True,
                   border_width=(5)),
         sg.Button('Detalle',
                   expand_x=True,
                   border_width=(5)),
                   ],
        [sg.Table(
            values=misActividades,
            headings=HEADER,
            alternating_row_color=sg.theme_input_background_color(),
            expand_x=True,
            expand_y=True,
            key='-TABLA-',
        )],
        [sg.Button('Crear Actividad',
                   font=('Arial italic',22),
                   border_width=(12),
                   expand_x=True
                   )]
    ]

    VALORES_FILTRO = [
        'Nombre de la actividad',
        'Autor de la actividad',
        'Pelea específica',
        'Actividad Privada',
        'Fecha de la actividad'
    ]
    DEFAULT_SEARCH = [
        ['No',
         'has',
        'seleccionado',
        'nada',
        'como',
        'filtro',
        ':(']
    ]

    SEARCH_DEF = [
        [sg.Text(f'Buscador',
                 font=('Arial bold',22),
                 pad=(50,10),
                 expand_x=True)],
        [sg.Text('Filtrar por: ',
                 pad=(25,5)),
         sg.Combo(values=VALORES_FILTRO,
                  size=(30,5),
                  font=(24),
                  readonly=True,
                  expand_x=True,
                  key='-FILTRO-'),
         sg.Text('Busqueda:',
                 pad=(25,5)),
         sg.InputText(size=(30,5),
                  font=(24),
                  expand_x=True,
                  key='-SEARCH-'),
         sg.Button('Buscar',
                   expand_x=True)],
        [sg.Text('Resultados: ',
                 font=('Arial bold',24),
                 justification='center',
                 expand_x=True)],
        [sg.Table(values=DEFAULT_SEARCH,
                  headings=HEADER,
                  expand_x=True,
                  expand_y=True,
                  alternating_row_color=sg.theme_input_background_color(),
                  key='-RSLTSEARCH-')],
        [sg.Button('Detalle Busqueda',
                   font=('Arial italic',22),
                   border_width=(12),
                   expand_x=True
                   )]
    ]

    types = db.getTypes()

    TYPE_DEF = [
        [sg.Text('Peleas disponibles',
                 font=('Arial bold',22),
                 pad=(50,10),
                 expand_x=True)],
        [sg.Text(f'Nombre: ',
                 pad=(25,5)),
         sg.Combo(values=types,
                  default_value='Seleccione una pelea',
                  expand_x= True,
                  font=(24),
                  readonly=True,
                  enable_events=True,
                  key='-TYPESEL-')],
        [sg.Text('',
                 pad=(50,10),
                 font=('Arial italic', 18),
                 key='-TYPENAME-')],
        [sg.Multiline('',
                      expand_y=True,
                      pad=(50,30),
                      key='-TYPEDESC-'),
         sg.Image(source=r'./img/Placeholder.png',
                  size=(720,405),
                  expand_x=True,
                  expand_y=True,
                  pad=(50,30),
                  key='-TYPEIMG-')]
    ]

    OPC_DEF = [
        [sg.Text('Opciones',
                 font=('Arial bold',22),
                 pad=(50,10),
                 expand_x=True)],
        [sg.Text('Dirección de la base de datos',
                 font=('Arial italic',18),
                 pad=(75,25)),
         sg.InputText(default_text=CONFIG['DATABASE']['hostname'],
                      pad=(75,25),
                      expand_x=True,
                      key='-CNFHOSTNAME-')],
        [sg.Text('Puerto de la base de datos',
                 font=('Arial italic',18),
                 pad=(75,25)),
         sg.InputText(default_text=CONFIG['DATABASE']['port'],
                      pad=(75,25),
                      expand_x=True,
                      key='-CNFPORT-')],
        [sg.Text(f'Su tema actual es: {cnf.getTheme()}',
                 font=('Arial italic',18),
                 pad=(75,25))],
        [sg.Listbox(values = sg.theme_list(),
                      font=('Arial',16),
                      pad=(75,25),
                      size =(45, 10),
                      expand_x=True,
                      expand_y=True,
                      default_values=cnf.getTheme(),
                      key ='-CNFTEMAS-',
                      enable_events = True)],
        [sg.Button('Aplicar configuración',
                   font=('Arial italic',22),
                   border_width=(12),
                   expand_x=True)]
    ]

    layout = [
        [sg.MenubarCustom(MENU_DEF, key='-MENUBAR-')],
        [sg.Text('When2Raid', 
                 size=(32,1), 
                 font=('Arial',28,'italic'),
                 background_color=sg.theme_text_color(),
                 text_color=sg.theme_background_color(),
                 justification='center', 
                 relief=sg.RELIEF_RIDGE,
                 expand_x=True,
                 key='-TITULO-')
        ],
        [sg.TabGroup([[
            sg.Tab('Pagina Principal',HOME_DEF),
            sg.Tab('Buscador',SEARCH_DEF),
            sg.Tab('Tipos disponibles',TYPE_DEF),
            sg.Tab('Opciones',OPC_DEF),
        ]],
        expand_x=True,
        expand_y=True,
        key='-TABS-'
        )]
    ]

    # Inicialización de la ventana
    window = sg.Window(
        'When2Raid',
        layout,size=(1424,812),
        font=('Arial'),
        resizable=True,
        finalize=True
    )

    return window

def setupActGUI():
    types = db.getTypes()

    sg.theme(cnf.getTheme())

    HORAS, MINUTOS = db.horaMin()

    ACT_DEF = [
        [sg.Text(f'Crea una nueva actividad',
                 justification='center',
                 size=(32,1),
                 relief=sg.RELIEF_RIDGE,
                 font=('Calibri italic',34))],
        [sg.Text('Nombre de la actividad:',
                 expand_x=True),
         sg.InputText(default_text='Actividad Nueva',
                      expand_x=True,
                      key='-ACTNAME-')],
        [sg.Text('Descripción de la actividad:')],
        [sg.MLine(default_text='Descripción...',
                  size=(35, 3),
                  expand_x=True,
                  key='-ACTDESC-')],
        [sg.Text('Tipo de actividad:')],
        [sg.Combo((types),
                  default_value=types[0],
                  size=(30,5),
                  font=(24),
                  readonly=True,
                  expand_x=True,
                  key='-ACTTYPE-')],
        [sg.Checkbox('¿Actividad Privada?',
                     expand_x=True,
                     key='-ACTPRIV-',
                     default=False)],
        [sg.Button('Fecha de la actividad',
                expand_x=True),
        sg.Text('No ha indicado ninguna fecha...',
                key='-CONFDATE-',
                font=(42),
                expand_x=True)],
        [sg.Text('Tus horas disponibles:',
                 expand_x=True)],
        [sg.Text('Hora Inicio:',
                 font=(42)),
        sg.Spin(values=HORAS,
                initial_value=HORAS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-HORAINICIO-'),
        sg.Text(':',font=(42)),
        sg.Spin(values=MINUTOS,
                initial_value=MINUTOS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-MINUTOSINICIO-')],
        [sg.Text('Hora Final:',
                 font=(42)),
        sg.Spin(values=HORAS,
                initial_value=HORAS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-HORAFINAL-'),
        sg.Text(':'),
        sg.Spin(values=MINUTOS,
                initial_value=MINUTOS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-MINUTOSFINAL-')],
        [sg.Button('Crear',
                   expand_x=True,
                   expand_y=True)],
        [sg.Text('',
                 key='-CONFACT-')]
    ]

    windowAct = sg.Window(
        'Crear Actividad', 
        layout=ACT_DEF,
        size=(612,462)
    )

    return windowAct

def loopActGUI(windowAct):
    VAL_MIN = {
        'HORA':     0,
        'MINUTOS':  0
        }
    VAL_MAX = {
        'HORA':     23,
        'MINUTOS':  59
            }            

    fechaAct = None
    while True:
        eventAct,valuesAct = windowAct.read()

        if eventAct == sg.WIN_CLOSED or eventAct == 'Cancelar':
            break    


        if valuesAct['-HORAINICIO-'] > VAL_MAX['HORA']:
            valuesAct['-HORAINICIO-'] = 0
        if valuesAct['-MINUTOSINICIO-'] > VAL_MAX['MINUTOS']:
            valuesAct['-MINUTOSINICIO-'] = 0

        if valuesAct['-HORAFINAL-'] < VAL_MIN['HORA']:
            valuesAct['-HORAFINAL-'] = 23
        if valuesAct['-MINUTOSFINAL-'] > VAL_MIN['MINUTOS']:
            valuesAct['-MINUTOSFINAL-'] = 59

        if eventAct == 'Fecha de la actividad':
            fechaAct = sg.popup_get_date()
            if fechaAct is not None:
                windowAct['-CONFDATE-'].update(f'Ha escogido el {fechaAct[1]} del {fechaAct[0]} de {fechaAct[2]}')
            else:
                windowAct['-CONFDATE-'].update(f'No ha especificado ninguna fecha...')

        if eventAct == 'Crear':
            try:
                NAME    = valuesAct['-ACTNAME-']
                DESC    = valuesAct['-ACTDESC-']
                TIPO    = db.getTypeID(valuesAct['-ACTTYPE-'])

                if valuesAct['-ACTPRIV-'] == True:
                    passwd = sg.popup_get_text('Indica la contraseña de la actividad',
                                                password_char='*')

                    HASH = db.passwdHash(passwd)
                else:
                    HASH = None

                if fechaAct is not None:
                    FECHA   = db.dateSQLFormat(fechaAct)
                else:
                    sg.popup('Debe escoger una fecha')
                    fechaAct = sg.popup_get_date()

                    FECHA = db.dateSQLFormat(fechaAct)

                HORA_INICIO = db.timeSQLFormat(valuesAct['-HORAINICIO-'],valuesAct['-MINUTOSINICIO-'])
                HORA_FINAL  = db.timeSQLFormat(valuesAct['-HORAFINAL-'],valuesAct['-MINUTOSFINAL-'])

                if db.addActividad(NAME,
                                DESC,
                                TIPO,
                                HASH,
                                FECHA,
                                HORA_INICIO,
                                HORA_FINAL):
                    return
                else:
                    windowAct['-CONFACT-'].update('Ha habido un error al crear la actividad')
            except Exception as e:
                print(e)
                sg.popup('Hay valores incorrectos en la actividad')
                continue

def setupEditGUI(act):
    types = db.getTypes()

    sg.theme(cnf.getTheme())

    HORAS, MINUTOS = db.horaMin()
    
    horasDisponibles    = db.getHorasDisponibles(act[0],act[6])
    horaInicio          = horasDisponibles[0][0:2]
    minutosInicio       = horasDisponibles[0][3:5]
    horaFinal           = horasDisponibles[1][0:2]
    minutosFinal        = horasDisponibles[1][3:5]

    EDIT_DEF = [
            [sg.Text(f'Edita una actividad',
                    justification='center',
                    size=(32,1),
                    relief=sg.RELIEF_RIDGE,
                    font=('Calibri italic',34))],
            [sg.Text('Nombre de la actividad:',                     
                    expand_x=True),
            sg.InputText(default_text=act[1],
                        expand_x=True,
                        key='-ACTNAME-')],
            [sg.Text('Descripción de la actividad:')],
            [sg.MLine(default_text=act[2],
                    size=(35, 3),
                    expand_x=True,
                    key='-ACTDESC-')],
            [sg.Text('Tipo de actividad:')],
            [sg.Combo((types),
                    default_value=act[3],
                    size=(30,5),
                    font=(24),
                    readonly=True,
                    expand_x=True,
                    key='-ACTTYPE-')],
            [sg.Checkbox('¿Actividad Privada?',
                        expand_x=True,
                        key='-ACTPRIV-',
                        default=act[4])],
            [sg.Button('Fecha de la actividad',
                    expand_x=True),
            sg.Text(act[5],
                    key='-CONFDATE-',
                    font=(42),
                    expand_x=True)],
            [sg.Text('Tus horas disponibles:',
                    expand_x=True)],
            [sg.Text('Hora Inicio:',
                    font=(42)),
            sg.Spin(values=HORAS,
                    initial_value=horaInicio,
                    enable_events=True,
                    readonly=False,
                    expand_x=True,
                    expand_y=True,
                    font=(42),
                    text_color=sg.theme_text_color(),
                    background_color=sg.theme_background_color(),                    
                    key='-HORAINICIO-'),
            sg.Text(':',font=(42)),
            sg.Spin(values=MINUTOS,
                    initial_value=minutosInicio,
                    enable_events=True,
                    readonly=False,
                    expand_x=True,
                    expand_y=True,
                    font=(42),
                    text_color=sg.theme_text_color(),
                    background_color=sg.theme_background_color(),                    
                    key='-MINUTOSINICIO-')],
            [sg.Text('Hora Final:',
                    font=(42)),
            sg.Spin(values=HORAS,
                    initial_value=horaFinal,
                    enable_events=True,
                    readonly=False,
                    expand_x=True,
                    expand_y=True,
                    font=(42),
                    text_color=sg.theme_text_color(),
                    background_color=sg.theme_background_color(),
                    key='-HORAFINAL-'),
            sg.Text(':'),
            sg.Spin(values=MINUTOS,
                    initial_value=minutosFinal,
                    enable_events=True,
                    readonly=False,
                    expand_x=True,
                    expand_y=True,
                    font=(42),
                    text_color=sg.theme_text_color(),
                    background_color=sg.theme_background_color(),
                    key='-MINUTOSFINAL-')],
            [sg.Button('Editar',
                    expand_x=True,
                    expand_y=True)],
            [sg.Text('',
                    key='-CONFACT-')]
        ]    
    
    window = sg.Window(
        'When2Raid',
        EDIT_DEF, 
        size=(612,462),
        font=('Arial'),
        resizable=True,
        finalize=True
    )

    return window

def loopEditGUI(windowEdit,actData):
        fechaEdit = misActividades[actData][5]
        while True:

            eventEdit,valuesEdit = windowEdit.read()                        

            if eventEdit == sg.WIN_CLOSED or eventEdit == 'Salir':
                break

            if eventEdit == 'Fecha de la actividad':
                fechaEdit = sg.popup_get_date()
                if fechaEdit is not None:
                    windowEdit['-CONFDATE-'].update(f'Ha escogido el {fechaEdit[1]} del {fechaEdit[0]} de {fechaEdit[2]}')
                else:
                    windowEdit['-CONFDATE-'].update(f'No ha especificado ninguna fecha...')

            if eventEdit == 'Editar':
                try:
                    ID_ACT  = misActividades[actData][0]
                    NAME    = valuesEdit['-ACTNAME-']
                    DESC    = valuesEdit['-ACTDESC-']
                    TIPO    = db.getTypeID(valuesEdit['-ACTTYPE-'])

                    if valuesEdit['-ACTPRIV-'] == True:
                        passwd = sg.popup_get_text('Indica la contraseña de la actividad',password_char='*')

                        HASH = db.passwdHash(passwd)
                    else:
                        HASH = None

                    if not isinstance(fechaEdit, datetime.date):
                        FECHA   = db.dateSQLFormat(fechaEdit)
                    else:
                        FECHA = fechaEdit.strftime('%Y-%m-%d')

                    HORA_INICIO = db.timeSQLFormat(valuesEdit['-HORAINICIO-'],valuesEdit['-MINUTOSINICIO-'])
                    HORA_FINAL  = db.timeSQLFormat(valuesEdit['-HORAFINAL-'],valuesEdit['-MINUTOSFINAL-'])

                    if db.updateActividad(ID_ACT,
                                            NAME,
                                            DESC,
                                            TIPO,
                                            HASH,
                                            FECHA,
                                            HORA_INICIO,
                                            HORA_FINAL):
                        break
                    else:
                        windowEdit['-CONFACT-'].update('Ha habido un error al crear la actividad')
                except:
                    sg.popup('Hay valores incorrectos en la actividad')
                    continue

def setupHorasGUI(act):
    sg.theme(cnf.getTheme())

    HORAS, MINUTOS = db.horaMin()

    if isinstance(act, int):
        idAct = act
    elif isinstance(act, (list, tuple)) and len(act) > 0:
        idAct = act[0]
    else:
        raise ValueError(f"Valor no esperado (qué haces tio.): {act}")
    
    horasDisponibles    = db.getHorasDisponibles(idAct,CONFIG['USER']['default'])
    if horasDisponibles is not None:
        horaInicio          = horasDisponibles[0][0:2]
        minutosInicio       = horasDisponibles[0][3:5]
        horaFinal           = horasDisponibles[1][0:2]
        minutosFinal        = horasDisponibles[1][3:5]    
    else:
        horaInicio          = '00'
        minutosInicio       = '00'
        horaFinal           = '00'
        minutosFinal        = '00'    

    HORAS_DEF = [
        [sg.Text()],
        [sg.Text('Hora Inicio:',
                font=(16)),
        sg.Spin(values=HORAS,
                initial_value=horaInicio,
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(16),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),                    
                key='-HORAINICIO-'),
        sg.Text(':',font=(16)),
        sg.Spin(values=MINUTOS,
                initial_value=minutosInicio,
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(32),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),                    
                key='-MINUTOSINICIO-')],
        [sg.Text('Hora Final:',
                font=(32)),
        sg.Spin(values=HORAS,
                initial_value=horaFinal,
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(32),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-HORAFINAL-'),
        sg.Text(':'),
        sg.Spin(values=MINUTOS,
                initial_value=minutosFinal,
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(32),
                text_color=sg.theme_text_color(),
                background_color=sg.theme_background_color(),
                key='-MINUTOSFINAL-')],
        [sg.Button('Editar',
                expand_x=True,
                expand_y=True)],
        [sg.Text('',
                key='-CONFACT-')]
    ]

    windowHoras = sg.Window('Editar Horas',
                            HORAS_DEF,
                            size=(412,212),
                            finalize=True)

    return windowHoras

def loopHorasGUI(act,windowsHoras):
    while True:
        eventHoras, valuesHoras = windowsHoras.read()

        if eventHoras == sg.WIN_CLOSED:
            break

        if eventHoras == 'Editar':
            try:
                horaInicio  = db.timeSQLFormat(valuesHoras['-HORAINICIO-'],valuesHoras['-MINUTOSINICIO-'])
                horaFinal   = db.timeSQLFormat(valuesHoras['-HORAFINAL-'],valuesHoras['-MINUTOSFINAL-'])

                if isinstance(act, int):
                    idAct = act
                elif isinstance(act, (list, tuple)) and len(act) > 0:
                    idAct = act[0]
                else:
                    raise ValueError(f"Valor no esperado (qué haces tio.): {act}")                

                if db.updateHorasDisponibles(idAct,CONFIG['USER']['default'],horaInicio,horaFinal):
                    sg.popup('Horas actualizadas correctamente')
                    break
                else:
                    sg.popup('Ha habido un error al actulizar tus horas')
                    continue
            except Exception as e:
                print(f'Error: {e}')

def setupDetailGUI(act):
    sg.theme(cnf.getTheme())

    LISTADO_HORAS = db.getAllHorasDisponibles(act)
    HEADINGS = [
        'Usuario',
        'Hora Inicio',
        'Hora Final'
    ]
    
    if isinstance(act, int):
        ACT         = db.getActInfo(act)
        ACT_INFO    = ACT[0]
    elif isinstance(act, (list, tuple)) and len(act) > 0:
        ACT         = db.getActInfo(act[0])
        ACT_INFO    = ACT[0]
    else:
        raise ValueError(f"Valor no esperado (qué haces tio.): {act}")         

    DETAIL_DEF = [
        [sg.Text(f'Detalle de la actividad "{ACT_INFO[1]}"',
                 justification='center',
                 relief=sg.RELIEF_RIDGE,
                 background_color=sg.theme_text_color(),
                 text_color=sg.theme_background_color(),                 
                 font=('Calibri italic',34),
                 expand_x=True)],
        [sg.Text(f'Descripción: {ACT_INFO[2]}',
                 pad=(50,10),
                 font=('Arial italic',16),
                 expand_x=True)],
        [sg.Text(f'Tipo de actividad: {db.getTypeName(ACT_INFO[3])}',
                 pad=(50,10),
                 font=('Arial italic',16),
                 expand_x=True)],
        [sg.Text(f'Fecha: {ACT_INFO[5]}',
                 pad=(50,10),
                 font=('Arial italic',16),
                 expand_x=True)],
        [sg.Table(values=LISTADO_HORAS,
                  headings=HEADINGS,
                  alternating_row_color=sg.theme_input_background_color(),
                  expand_x=True,
                  expand_y=True,
                  font=('Arial',22),
                  key='-TABLA-')],
        [sg.Button('Apuntarse',
                   font=('Arial italic',22),
                   border_width=(12),
                   expand_x=True,
                   expand_y=True)],
        [sg.Text('',
                 pad=(25,5),
                 key='-CONFAPT-',)]
    ]

    windowDetail = sg.Window('Detalles de la actividad',
                             DETAIL_DEF,
                             size=(1024,712),
                             font=('Arial'),
                             finalize=True,)
    
    return windowDetail

def loopDetailGUI(windowDetail,actID):
    actData = db.getActInfo(actID)
    while True:
        eventDetail, valuesDetails = windowDetail.read()

        if eventDetail == sg.WIN_CLOSED or eventDetail == 'Salir':
            break

        if eventDetail == 'Apuntarse':
            if actData[0][4] is not None:
                tryPasswd = sg.popup_get_text('Indica la contraseña de la actividad:')
                if db.passwdHash(tryPasswd) == actData[0][4]:
                    windowHoras = setupHorasGUI(actID)
                    loopHorasGUI(actID,windowHoras)

                    windowHoras.close()

                    windowDetail.close()
                    windowDetail = setupDetailGUI(actID)
                else:
                    sg.popup('Contraseña incorrecta')
            else:
                windowHoras = setupHorasGUI(actID)
                loopHorasGUI(actID,windowHoras)

                windowHoras.close()

                windowDetail.close()
                windowDetail = setupDetailGUI(actID)                

def resizeImg(inputImage,outputImage,ancho,alto):
    original_image = Image.open(inputImage)
    resized_image = original_image.resize((ancho, alto))
    resized_image.save(outputImage)

def main():
    global CONFIG, misActividades
    CONFIG = cnf.getCnf()
    actApuntado         = db.getApuntadas(CONFIG['USER']['default'])
    listaActividades    = [list(x) for x in actApuntado]
    misActividades = db.formatActSelect(listaActividades) 

    window = setupMainGUI()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Salir':
            break

        if event == 'Cerrar Sesión':
            window.close()
            cnf.defaultUser('')
            lg.main()
            break
        # Eventos TAB Actividades
        if event == 'Editar':
            try:
                actData = values['-TABLA-'][0]
                if db.autorAct(misActividades[actData][0]):
                    windowEdit = setupEditGUI(misActividades[actData])
                    loopEditGUI(windowEdit,actData)

                    windowEdit.close()

                    window.close()
                    main()
                else:
                    windowHoras = setupHorasGUI(misActividades[actData])
                    loopHorasGUI(misActividades[actData],windowHoras)

                    windowHoras.close()

                    window.close()
                    main()                 
            except IndexError:
                sg.popup('No ha seleccionado ninguna actividad')
            except Exception as e:
                sg.popup('Error espcificando actividad')
                print(f'Error: {e}')

        if event == 'Borrar':
            try:
                actData = values['-TABLA-'][0]
                if db.autorAct(misActividades[actData][0]):
                    if sg.popup_yes_no('¿Estás seguro de que quieres borrar esta actividad?') == 'Yes':
                        if db.deleteAct(misActividades[actData][0]):
                            sg.popup('Se ha borrardo correctamente la actividad')                        

                            window.close()
                            main()
                else:
                    if sg.popup_yes_no('¿Estás seguro de que quieres desapuntarte de esta actividad?') == 'Yes':
                        if db.delHoras(misActividades[actData][0],CONFIG['USER']['default']):
                            sg.popup('Te has desapuntado correctamente de la actividad')

                            window.close()
                            main()
            except IndexError:
                sg.popup('No ha seleccionado ninguna actividad')
            except Exception as e:
                sg.popup('Eror espcificando actividad')
                print(f'Error: {e}')

        if event == 'Detalle':
            try:
                actData = values['-TABLA-'][0]
                windowDetail = setupDetailGUI(misActividades[actData])
                loopDetailGUI(windowDetail,actData)

                windowDetail.close()
            except Exception as e:
                sg.popup('Error detallando la actividad')
                print(f'Error:{e}')

        if event == 'Crear Actividad':
            windowAct = setupActGUI()
            loopActGUI(windowAct)

            windowAct.close()

            window.close()
            main()
        # Eventos Busqueda
        if event == 'Buscar':
            if values['-FILTRO-'] == 'Nombre de la actividad':
                rsltBusqueda = db.nameSearch(values['-SEARCH-'])
                listaBusqueda = db.formatActSelect(rsltBusqueda)

                window['-RSLTSEARCH-'].update(values=listaBusqueda)
            if values['-FILTRO-'] == 'Autor de la actividad':
                rsltBusqueda = db.authorSearch(values['-SEARCH-'])
                listaBusqueda = db.formatActSelect(rsltBusqueda)

                window['-RSLTSEARCH-'].update(values=listaBusqueda)
            if values['-FILTRO-'] == 'Pelea específica':
                rsltBusqueda = db.typeSearch(values['-SEARCH-'])
                listaBusqueda = db.formatActSelect(rsltBusqueda)

                window['-RSLTSEARCH-'].update(values=listaBusqueda)
            if values['-FILTRO-'] == 'Actividad Privada':
                rsltBusqueda = db.privateSearch(values['-SEARCH-'])
                listaBusqueda = db.formatActSelect(rsltBusqueda)

                window['-RSLTSEARCH-'].update(values=listaBusqueda)

            if values['-FILTRO-'] == 'Fecha de la actividad':
                rsltBusqueda = db.dateSearch(values['-SEARCH-'])
                listaBusqueda = db.formatActSelect(rsltBusqueda)

                window['-RSLTSEARCH-'].update(values=listaBusqueda)

        if event == 'Detalle Busqueda':
            try:
                idRowTabla      = values['-RSLTSEARCH-'][0]
                actData         = rsltBusqueda[idRowTabla][0]
                windowDetail    = setupDetailGUI(actData)
                loopDetailGUI(windowDetail,actData)

                windowDetail.close()

                window.close()
                main()
            except Exception as e:
                sg.popup('Error detallando la actividad')
                print(f'Error:{e}')            
        # Eventos Tipos
        if values['-TYPESEL-'] != 'Seleccione una pelea':
            typeInfo = db.getTypeInfo(values['-TYPESEL-'])
            window['-TYPENAME-'].update(typeInfo[0][0])
            window['-TYPEDESC-'].update(typeInfo[0][1])
            

            filename = './img/' + typeInfo[0][0] + '.png'
            resizeImg(filename,filename,720,405)
            window['-TYPEIMG-'].update(source=filename)
        # Eventos Opciones
        if event == 'Aplicar configuración':
            cnf.writeConfig(values['-CNFHOSTNAME-'],values['-CNFPORT-'],values['-CNFTEMAS-'])
            sg.popup('El programa se reinicará con la configuración especificada')

            window.close()
            lg.main()
if __name__ == '__main__':
    main()