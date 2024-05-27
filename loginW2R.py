import PySimpleGUI as sg
import dbW2R as db
import configW2R as cnf

def setupMainGUI():
    sg.theme(cnf.getTheme())
    # Esquema de la ventana
    layout = [
        [sg.Text("Nombre de usuario:")],
        [sg.Input(key='-USER-')],
        [sg.Text("Contraseña")],
        [sg.Input(key='-PASS-',password_char='*')],
        [sg.Button('Iniciar Sesión'),sg.Button('Crear Usuario'),sg.Button('Configuración BBDD')],
        [sg.Text('',key='-CONF-')] # Muestra de mensajes 
    ]

    # Creamos la ventana
    window = sg.Window('Iniciar Sesión',layout,return_keyboard_events=True)

    return window

def setupUserGUI():
    sg.theme(cnf.getTheme())
    # Ventana de creación de usuario
    layoutUser = [
        [sg.Text("Nombre de usuario:")],
        [sg.Input(key='-USER-')],
        [sg.Text("Contraseña")],
        [sg.Input(key='-PASS-',password_char='*')],
        [sg.Text("Nombre Completo")],
        [sg.Input(key='-FULLNAME-')],
        [sg.Button('Crear Usuario')],
        [sg.Text('',key='-CONF-')] # Muestra de mensajes 
    ]

    windowUser = sg.Window('Iniciar Sesión',layoutUser,return_keyboard_events=True)

    return windowUser

def main():
    window = setupMainGUI()

    while True:
        event, values = window.read()

        if event == 'Iniciar Sesión' and values['-PASS-'] != '':
            global cnxDB

            userHash = db.passwdHash(values['-PASS-'])

            if db.checkLogin(values['-USER-'],userHash):
                cnxDB = db.loginDB()

                if cnxDB is not None:
                    window['-CONF-'].update(f'Ha iniciado sesión correctamente con:{values['-USER-']}')
                    cnf.defaultUser(values['-USER-'])

            else:
                window['-CONF-'].update('Nombre de usuario o contraseña incorrecto')

        if event == 'Configuración BBDD':
            cnf.main()

        if event == 'Crear Usuario':
            windowUser = setupUserGUI()
            # Generamos una nueva ventana
            while True:
                eventUser, valuesUser = windowUser.read()

                if eventUser == 'Crear Usuario' and valuesUser['-PASS-'] != '':
                    if db.checkUser(valuesUser['-USER-']) is False:
                        userHash = db.passwdHash(valuesUser['-PASS-'])

                        if db.addUsr(valuesUser['-USER-'],userHash,valuesUser['-FULLNAME-']):
                            windowUser['-CONF-'].update('Usuario creado correctamente')
                        else:
                            windowUser['-CONF-'].update('Error en la creación del usuario')
                    else:
                        windowUser['-CONF-'].update('Usuario ya existente')
                    
                if eventUser == sg.WIN_CLOSED:
                    break

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

if __name__ == '__main__':
    main()