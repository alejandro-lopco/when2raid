import configparser as ini
import PySimpleGUI as sg

def writeConfig(hostname,puerto,tema):
    config = ini.ConfigParser()

    config['DATABASE'] = {
        'hostname': f'{hostname}',
        'port': f'{puerto}'
    }

    config['USER'] = {
        'default': ''
    }

    config['THEME'] = {
        'tema' : ''.join(tema) # Chapuza histórica pero funciona
    }

    with open('configW2R.ini','w') as file:
        config.write(file)

def getCnf():
    config = ini.ConfigParser()
    config.read('configW2R.ini')

    return config

def defaultUser(username):
    config = ini.ConfigParser()

    config.read('configW2R.ini')

    if 'USER' not in config.sections():
        config.add_section('USER')
    
    config.set('USER','default',username)

    with open('configW2R.ini','w') as file:
        config.write(file)

def getTheme():
    config = ini.ConfigParser()
    config.read('configW2R.ini')

    return str(config['THEME']['tema'])

def setupGUI():
    config = getCnf()
    # Esquema de la ventana
    sg.theme(getTheme())

    layout = [
        [sg.Text("Hostname de la base de datos:")],
        [sg.Input(key='-HOSTNAME-',default_text=config['DATABASE']['hostname'])],
        [sg.Text("Puerto")],
        [sg.Input(key='-PUERTO-',default_text=config['DATABASE']['port'])],
        [sg.Text("Tema de la aplcicación!")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 4),
                      expand_x=True,
                      default_values=getTheme(),
                      key ='-TEMAS-',
                      enable_events = True)],
        [sg.Button('Guardar Configuración')],
        [sg.Text('',key='-CONF-')]
    ]

    # Creamos la ventana
    window = sg.Window('Configuración When2Raid',layout)

    return window

def main():
    window = setupGUI()
    
    while True:
        event, values = window.read()

        if event == 'Guardar Configuración':
            writeConfig(values['-HOSTNAME-'],values['-PUERTO-'],values['-TEMAS-'])

            sg.popup('El programa se reinicará con la configuración especificada')
            window.close()

            window = setupGUI()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

if __name__ == '__main__':
    conf = getCnf()
    main()