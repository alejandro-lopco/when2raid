import PySimpleGUI as sg
import mysql.connector
import dbW2R as db
import configW2R as cnf
from mysql.connector import Error

CONFIG = cnf.getCnf()

def setupMainGUI():
    sg.theme(cnf.getTheme())

    header = ['ID','Titulo']
    test = []
    for x in range (0,50): # Valores de testeo
        test += [x,f'Entrada #{x}'],
    # Definición de opciones en la toolbar
    MENU_DEF = [
        ['&Aplicación',['&Salir','&Cerrar Sesión']],
        ['&Actividades',['&Crear Actividad']] 
    ]

    HOME_DEF = [
        [sg.Text(f'Bienvenido {CONFIG['USER']['default']}')],
        [sg.Text('Tus actividades:'),sg.Button('Crear Actividad')],
        [sg.Table(
            values=test,
            headings=header,
            num_rows=6,
            alternating_row_color='black',
            expand_x=True,
            key='-TABLA-',
        )]
    ]

    SEARCH_DEF = [
        [sg.Text('Buscador')],
        [sg.Text('Resultados: ')], 
        [sg.Table(
            values=test,
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
            values=test,
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
            values=test,
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
                 font=('Calibri',32,'italic'),
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
        key='-TABS-',
        expand_x=True,
        )]
    ]

    # Inicialización de la ventana
    window = sg.Window(
        'When2Raid',
        layout,size=(1024,512),
        font=('Calibri'),
        resizable=True,
        finalize=True,
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
        [sg.Button('Fecha de la actividad:',
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

def main():
    window = setupMainGUI()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break        

        if event == 'Crear Actividad':
            windowAct = setupActGUI()

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
                        FECHA   = db.dateSQLFormat(valuesAct['-DATEACT-'])

                    if db.addActividad(NAME,DESC,TIPO,HASH,FECHA):
                        windowAct.close()
                    else:
                        windowAct['-CONFACT-'].update('Ha habido un error al crear la actividad')

                if eventAct == sg.WIN_CLOSED or eventAct == 'Cancelar':
                    break
            
if __name__ == '__main__':
    main()