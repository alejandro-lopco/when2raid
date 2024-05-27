import PySimpleGUI as sg
import mysql.connector 
import configW2R as cnf
from mysql.connector import Error

def setupMainGUI():
    sg.theme(cnf.getTheme())

    header = ['ID','Titulo']
    test = []
    for x in range (0,50):
        test += [x,f'Entrada #{x}'],
    # Definición de opciones en la toolbar
    MENU_DEF = [
        ['&Aplicación',['&Salir','&Cerrar Sesión']],
        ['&Actividades',['&Crear Actividad']] 
    ]

    HOME_DEF = [
        [sg.Text('Bienvenido #USUARIO#')],
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
        [sg.Titlebar('When2Raid')],
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

def main():
    window = setupMainGUI()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break        

if __name__ == '__main__':
    main()