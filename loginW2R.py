import PySimpleGUI as sg
import dbW2R as db
import configW2R as cnf

def setupMainGUI():
    # Esquema de la ventana
    layout = [
        [sg.Text("Nombre de usuario:")],
        [sg.Input(key='-USER-')],
        [sg.Text("Contraseña")],
        [sg.Input(key='-PASS-')],
        [sg.Button('Iniciar Sesión'),sg.Button('Crear Usuario'),sg.Button('Configuración BBDD')],
        [sg.Text('',key='-CONF-')] # Muestra de mensajes 
    ]

    # Creamos la ventana
    window = sg.Window('Iniciar Sesión',layout)

    return window

def setupUserGUI():
    # Ventana de creación de usuario
    layoutUser = [
        [sg.Text("Nombre de usuario:")],
        [sg.Input(key='-USER-')],
        [sg.Text("Contraseña")],
        [sg.Input(key='-PASS-')],
        [sg.Text("Nombre Completo")],
        [sg.Input(key='-FULLNAME-')],
        [sg.Button('Crear Usuario')],
        [sg.Text('',key='-CONF-')] # Muestra de mensajes 
    ]

    windowUser = sg.Window('Iniciar Sesión',layoutUser)

    return windowUser

def main():
    window = setupMainGUI()

    while True:
        event, values = window.read()

        if event == 'Iniciar Sesión':
            global confDB

            if db.checkLogin(values['-USER-'],values['-PASS-']):
                confDB = db.loginDB(values['-USER-'],values['-PASS-'])

                window['-CONF-'].update('Ha iniciado sesión correctamente')
                window['-CONF-'].update(text_color='Light Green')

            else:
                window['-CONF-'].update('Nombre de usuario o contraseña incorrecto')
                window['-CONF-'].update(text_color='Black')

        if event == 'Configuración BBDD':
            cnf.main()

        if event == 'Crear Usuario':
            windowUser = setupUserGUI()
            # Cambio completo del layout previo
            while True:
                eventUser, valuesUser = windowUser.read()

                if eventUser == 'Crear Usuario':
                    if db.checkUser(windowUser['-USER-']):
                        db.addUsr(windowUser['-USER-'],windowUser['-PASS-'],windowUser['-FULLNAME-'])
                    else:
                        windowUser['-CONF-'].update('Usuario ya existente')
                        windowUser['-CONF-'].update(text_color='Black')

                if eventUser == sg.WIN_CLOSED:
                    break

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

if __name__ == '__main__':
    main()