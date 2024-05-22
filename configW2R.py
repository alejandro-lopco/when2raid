import configparser as ini
import PySimpleGUI as sg

def writeConfig(hostname,puerto):
    config = ini.ConfigParser()

    config['DATABASE'] = {
        'hostname': hostname,
        'port': puerto
    }

    with open('configW2R.ini','w') as file:
        config.write(file)

def getCnf():
    config = ini.ConfigParser()
    config.read('configW2R.ini')

    return config


def setupGUI():
    # Esquema de la ventana
    layout = [
        [sg.Text("Hostname de la base de datos:")],
        [sg.Input(key='-HOSTNAME-',default_text=conf['DATABASE']['hostname'])],
        [sg.Text("Puerto")],
        [sg.Input(key='-PUERTO-',default_text=conf['DATABASE']['port'])],
        [sg.Button('Guardar Configuración')],
        [sg.Text('',key='-CONF-')]
    ]

    # Creamos la ventana
    window = sg.Window('Entrega #3',layout)

    return window

def main():
    window = setupGUI()
    
    while True:
        event, values = window.read()

        if event == 'Guardar Configuración':
            writeConfig(values['-HOSTNAME-'],values['-PUERTO-'])
            window['-CONF-'].update('Se ha actualizado correcatamente la configuración')
            window['-CONF-'].update(text_color='Light Green')

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break

if __name__ == '__main__':
    conf = getCnf()
    main()