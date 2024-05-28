import PySimpleGUI as sg
import mysql.connector
import dbW2R as db
import configW2R as cnf
from mysql.connector import Error

def setupMainGUI():
    config = cnf.getCnf()

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
        [sg.Text(f'Bienvenido {config['USER']['default']}')],
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
    config = cnf.getCnf()

    types = db.getTypes()

    sg.theme(cnf.getTheme())

    ACT_DEF = [
        [sg.Text(f'Crea una nueva actividad',
                 justification='center',
                 size=(32,1),
                 relief=sg.RELIEF_RIDGE,
                 font=('Calibri italic',24))],
        [sg.Text('Nombre de la actividad',
                 size=(16,1)),
         sg.InputText(default_text='Actividad Nueva',
                      expand_x=True,
                      key='-ACTNAME-')],
        [sg.Text('Descripción de la actividad')],
        [sg.MLine(default_text='Descripción...',
                  size=(35, 3),
                  expand_x=True,
                  key='-ACTDESC-')],
        [sg.Text('Descripción de la actividad')],
        [sg.Combo((types),
                  size=(30,5),
                  readonly=True,
                  expand_x=True,
                  key='-ACTTYPE-')]
    ]

    windowAct = sg.Window(
        'Crear Actividad', 
        layout=ACT_DEF,
        size=(512,612)
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
                if eventAct == sg.WIN_CLOSED or eventAct == 'Cancelar':
                    break        
            
if __name__ == '__main__':
    main()