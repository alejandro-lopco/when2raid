import PySimpleGUI as sg
import loginW2R as lg
import dbW2R as db
import configW2R as cnf

def setupMainGUI():
    global CONFIG
    CONFIG = cnf.getCnf()
    sg.theme(cnf.getTheme())

    # Definición de opciones en la toolbar
    MENU_DEF = [
        ['&Aplicación',['&Salir','&Cerrar Sesión']],
        ['&Actividades',['&Crear Actividad']] 
    ]

    header = [
        'ID',
        'Nombre',
        'Descripción',
        'Pelea',
        'Privada',
        'Fecha'
    ]
    actApuntado         = db.getApuntadas(CONFIG['USER']['default'])
    listaActividades    = [list(x) for x in actApuntado]
    misActividades      = []
    for x in listaActividades:
        actInfo = db.getActInfo(x[0])
        listaInfo = [list(y) for y in actInfo]

        if listaInfo[0][4] is not None:
            listaInfo[0][4] = True
        else:
            listaInfo[0][4] = False

        listaInfo[0][3] = db.getTypeName(listaInfo[0][3])

        misActividades += listaInfo

    HOME_DEF = [
        [sg.Text(f'Bienvenido {CONFIG['USER']['default']}',
                 font=('Arial bold',22),
                 pad=(50,10),
                 expand_x=True)],
        [sg.Text('Tus actividades:'),
         sg.Button('Editar Actividad',
                   expand_x=True,
                   border_width=(5))],
        [sg.Table(
            values=misActividades,
            headings=header,
            alternating_row_color='black',
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

    SEARCH_DEF = [
        [sg.Text('Buscador')],
        [sg.Text('Resultados: ')], 
        [sg.Table(
            values=misActividades,
            headings=header,
            num_rows=6,
            alternating_row_color='black',
            expand_x=True,
            key='-TABLA-',
        )]
    ]

    TYPE_DEF = [
        [sg.Text('Tipos disponibles')],
        [sg.Text(': ')], 
        [sg.Table(
            values=misActividades,
            headings=header,
            num_rows=6,
            alternating_row_color='black',
            expand_x=True,
            key='-TABLA-',
        )]
    ]

    OPC_DEF = [
        [sg.Text('Opciones')],
        [sg.Text('Resultados: ')], 
        [sg.Table(
            values=misActividades,
            headings=header,
            num_rows=6,
            alternating_row_color='black',
            expand_x=True,
            key='-TABLA-',
        )]
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
        layout,size=(1024,512),
        font=('Arial'),
        resizable=True,
        finalize=True
    )

    return window

def setupActGUI():
    types = db.getTypes()

    sg.theme(cnf.getTheme())

    HORAS   = [x for x in range(0,24)]
    MINUTOS = [y for y in range(0,60)]

    VAL_MAX = {
        'HORA'  : (0,23),
        'MIN'   : (0,59)
    }

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
                  default_value='The Epic of Alexander (Ultimate)',
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
                key='-HORAINICIO-'),
        sg.Text(':',font=(42)),
        sg.Spin(values=MINUTOS,
                initial_value=MINUTOS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
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
                key='-HORAFINAL-'),
        sg.Text(':'),
        sg.Spin(values=MINUTOS,
                initial_value=MINUTOS[0],
                enable_events=True,
                readonly=False,
                expand_x=True,
                expand_y=True,
                font=(42),
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

def setupEditGUI():
    pass

def main():
    window = setupMainGUI()

    while True:
        event, values = window.read()
        print(event)
        print(values)

        if event == sg.WIN_CLOSED or event == 'Salir':
            break

        if event == 'Cerrar Sesión':
            window.close()
            cnf.defaultUser('')
            lg.main()
            break

        if event == 'Editar Actividad':
            try:
                if db.autorAct(values['-TABLA-'][0]):
                    print("Vas a editar")

    #                while True:
    #                    eventAct,valuesAct = windowEdit.read()
                else:
                    sg.popup('No eres el autor de esta actividad.')
            except IndexError:
                sg.popup('No ha seleccionado ninguna actividad')
        if event == 'Crear Actividad':
            windowAct = setupActGUI()

            fechaAct = None
            while True:
                eventAct,valuesAct = windowAct.read()

                if eventAct == 'Fecha de la actividad':
                    fechaAct = sg.popup_get_date()
                    if fechaAct is not None:
                        windowAct['-CONFDATE-'].update(f'Ha escogido el {fechaAct[1]} del {fechaAct[0]} de {fechaAct[2]}')
                    else:
                        windowAct['-CONFDATE-'].update(f'No ha especificado ninguna fecha...')

                if eventAct == 'Crear':

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

                    HORA_INICIO = db.timeSQLFormat(valuesAct['-HORAINICIO-'],valuesAct['-MINUTOSINICIO-'])
                    HORA_FINAL  = db.timeSQLFormat(valuesAct['-HORAFINAL-'],valuesAct['-MINUTOSFINAL-'])

                    print(NAME,DESC,TIPO,HASH,FECHA,HORA_INICIO,HORA_FINAL)

                    if db.addActividad(NAME,DESC,TIPO,HASH,FECHA,HORA_INICIO,HORA_FINAL):
                        windowAct.close()

                        window.close()
                        window = setupMainGUI()
                    else:
                        windowAct['-CONFACT-'].update('Ha habido un error al crear la actividad')

                if eventAct == sg.WIN_CLOSED or eventAct == 'Cancelar':
                    break

if __name__ == '__main__':
    main()