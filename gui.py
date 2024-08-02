import customtkinter
import configparser
import threading
import os
import signal

from GPDX303S import PowerSupply
import programmer

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('dark-blue')

ini_path = r'C:\CCAR_Programming_Bench\__settings__\settings.ini'
config = configparser.ConfigParser()
config.read(ini_path)
config_section = config['Config']

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # init
        self.ps = PowerSupply(config['Config']['COMM_powersupply'])
        self.choose_command = 'Choose command'
        self.connect_mode = 'USB'

        # window
        self.title('CCAR Programming Bench')
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0), weight=1)

        # sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text='Club Car Programming', font=customtkinter.CTkFont(size=14, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # UUT Control OptionMenu
        self.sidebar_optionmenu_UUT_control = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                            values=['UUT OFF', 'UUT ON'], command=self.control_powersupply)
        self.sidebar_optionmenu_UUT_control.grid(row=1, column=0, padx=20, pady=(20, 10))

        # New OptionMenu for USB or WiFi
        self.sidebar_optionmenu_connection = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                            values=['USB', 'WiFi'], command=self.change_connection_type)
        self.sidebar_optionmenu_connection.grid(row=2, column=0, padx=20, pady=(20, 10))

        # Commands OptionMenu
        self.sidebar_optionmenu_commands = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=True,
                                                values=['Choose command', 'Program Android', 'Program STM',
                                                        'Program GPS', 'Program Modem', 'Version Android', 
                                                        'Version STM', 'Version GPS', 'Version Modem'],
                                                command=self.change_selection)
        self.sidebar_optionmenu_commands.grid(row=3, column=0, padx=20, pady=(20, 10))

        # Run Command Button
        self.sidebar_button_run = customtkinter.CTkButton(self.sidebar_frame, text='Run Command', command=self.run_operation)
        self.sidebar_button_run.grid(row=4, column=0, padx=20, pady=(20, 10))

        # Configuration Button
        self.sidebar_button_config = customtkinter.CTkButton(self.sidebar_frame, text='Configuration', command=self.open_config_window)
        self.sidebar_button_config.grid(row=5, column=0, padx=20, pady=(20, 10))

        # Stop ALL Button
        self.sidebar_button_exit = customtkinter.CTkButton(self.sidebar_frame, text="Stop ALL", command=self.quit_app)
        self.sidebar_button_exit.grid(row=6, column=0, padx=20, pady=(20, 10))
        
        # textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan = 2, padx=(20, 20), pady=(20, 20), sticky='nsew')
        self.textbox.configure(state='disabled') # read only

    def open_config_window(self):
        config_window = customtkinter.CTkToplevel(self)
        config_window.title('Configuration')
        config_window.geometry('900x500')
        config_window.attributes('-topmost', True)

        # Frame for COMM PowerSupply
        frame_comm = customtkinter.CTkFrame(config_window)
        frame_comm.pack(padx=20, pady=10, fill='x')

        label_comm = customtkinter.CTkLabel(frame_comm, text='COMM PowerSupply:')
        label_comm.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_comm = customtkinter.CTkEntry(frame_comm, width=400)
        entry_comm.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_comm.insert(0, config_section['COMM_powersupply'])
        
        # Frame for IP
        frame_ip = customtkinter.CTkFrame(config_window)
        frame_ip.pack(padx=20, pady=10, fill='x')

        label_ip = customtkinter.CTkLabel(frame_ip, text='IP Address:')
        label_ip.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_ip = customtkinter.CTkEntry(frame_ip, width=400)
        entry_ip.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_ip.insert(0, config_section['ip'])

        # Frame for FW Android
        frame_android = customtkinter.CTkFrame(config_window)
        frame_android.pack(padx=20, pady=10, fill='x')

        label_android = customtkinter.CTkLabel(frame_android, text='FW Android folder:')
        label_android.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_android = customtkinter.CTkEntry(frame_android, width=400)
        entry_android.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_android.insert(0, config_section['fw_android_folder'])

        label_android_version = customtkinter.CTkLabel(frame_android, text='Version:')
        label_android_version.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        entry_android_version = customtkinter.CTkEntry(frame_android, width=200)
        entry_android_version.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        entry_android_version.insert(0, config_section['version_android'])

        # Frame for STM
        frame_stm = customtkinter.CTkFrame(config_window)
        frame_stm.pack(padx=20, pady=10, fill='x')

        label_stm = customtkinter.CTkLabel(frame_stm, text='STM file:')
        label_stm.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_stm = customtkinter.CTkEntry(frame_stm, width=400)
        entry_stm.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_stm.insert(0, config_section['stm_file'])

        label_stm_version = customtkinter.CTkLabel(frame_stm, text='Version:')
        label_stm_version.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        entry_stm_version = customtkinter.CTkEntry(frame_stm, width=200)
        entry_stm_version.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        entry_stm_version.insert(0, config_section['version_stm'])

        # Frame for GPS
        frame_gps = customtkinter.CTkFrame(config_window)
        frame_gps.pack(padx=20, pady=10, fill='x')

        label_gps = customtkinter.CTkLabel(frame_gps, text='GPS file:')
        label_gps.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_gps = customtkinter.CTkEntry(frame_gps, width=400)
        entry_gps.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_gps.insert(0, config_section['gps_file'])

        label_gps_version = customtkinter.CTkLabel(frame_gps, text='Version:')
        label_gps_version.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        entry_gps_version = customtkinter.CTkEntry(frame_gps, width=300)
        entry_gps_version.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        entry_gps_version.insert(0, config_section['version_gps'])

        # Frame for Modem
        frame_modem = customtkinter.CTkFrame(config_window)
        frame_modem.pack(padx=20, pady=10, fill='x')

        label_modem_version = customtkinter.CTkLabel(frame_modem, text='Modem Version:')
        label_modem_version.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        entry_modem_version = customtkinter.CTkEntry(frame_modem, width=200)
        entry_modem_version.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        entry_modem_version.insert(0, config_section['version_modem'])

        def save_config():
            config['Config']['comm_powersupply'] = entry_comm.get()
            config['Config']['ip'] = entry_ip.get()
            config['Config']['fw_android_folder'] = entry_android.get()
            config['Config']['version_android'] = entry_android_version.get()
            config['Config']['stm_file'] = entry_stm.get()
            config['Config']['version_stm'] = entry_stm_version.get()
            config['Config']['gps_file'] = entry_gps.get()
            config['Config']['version_gps'] = entry_gps_version.get()
            config['Config']['version_modem'] = entry_modem_version.get()
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
            config_window.destroy()
            self.add_text_log('Settings have been modified')

        save_button = customtkinter.CTkButton(config_window, text='Save new configuration', command=save_config)
        save_button.pack(pady=20)

        # Label for developer information
        dev_label = customtkinter.CTkLabel(config_window, text='Developed by Javier Benitez')
        dev_label.pack(pady=10, anchor='s')

    def change_selection(self, select_operation: str):
        self.choose_command = select_operation

    def run_operation(self):
        self.choose_command = self.sidebar_optionmenu_commands.get()
        if self.choose_command == 'Choose command':
            self.add_text_log('Select an action')
        else:
            self.add_text_log(f'Selected {self.choose_command}')
            
            def output(output):
                output = output.strip()
                match self.choose_command:
                    case 'Version Android':
                        self.add_text_log('Version correct') if output == config['Config']['version_android'] else self.add_text_log('Version incorrect')
                    case 'Version STM':
                        self.add_text_log('Version correct') if output == config['Config']['version_stm'] else self.add_text_log('Version incorrect')
                    case 'Version GPS':
                        self.add_text_log('Version correct') if output == config['Config']['version_gps'] else self.add_text_log('Version incorrect')
                    case 'Version Modem':
                        self.add_text_log('Version correct') if output == config['Config']['version_modem'] else self.add_text_log('Version incorrect')

            match self.choose_command:
                case 'Program Android':
                    threading.Thread(target=programmer.prog_android, args=(self.add_text_log, output)).start()
                case 'Program STM':
                    threading.Thread(target=programmer.prog_stm_stlink, args=(self.add_text_log, output)).start()
                case 'Program GPS':
                    threading.Thread(target=programmer.prog_gps, args=(self.add_text_log, output)).start()
                case 'Program Modem':
                    threading.Thread(target=programmer.prog_modem, args=(self.add_text_log, output)).start()
                case 'Version Android':
                    threading.Thread(target=programmer.check_android, args=(self.add_text_log, output)).start()
                case 'Version STM':
                    threading.Thread(target=programmer.check_stm, args=(self.add_text_log, output)).start()
                case 'Version GPS':
                    threading.Thread(target=programmer.check_gps, args=(self.add_text_log, output)).start()
                case 'Version Modem':
                    threading.Thread(target=programmer.check_modem, args=(self.add_text_log, output)).start()

    def control_powersupply(self, ps_state: str):
        self.output_ps(ps_state)
        
    def quit_app(self):
        os.kill(os.getpid(), signal.SIGTERM)

    def add_text_log(self, text):
        self.textbox.configure(state='normal')
        self.textbox.insert('end', text + "\n")
        self.textbox.configure(state='disabled')
        self.textbox.yview_moveto(1)

    ### Functions for control
    def output_ps(self, ps_state):
        self.ps.open()
        if ps_state == 'UUT ON':
            self.ps.set_voltage(1, 5)
            self.ps.set_current(1, 0.5)
            self.ps.set_output(1)
            self.add_text_log('Powersupply output is on')
        else:
            self.ps.set_output(0)
            self.add_text_log('Powersupply output is off')
        self.ps.close()

    def change_connection_type(self, mode: str):
        def output(output):
                output = output.strip()
        if mode == 'USB':
            threading.Thread(target=programmer.connect_usb, args=(self.add_text_log, output)).start()
        else:
            threading.Thread(target=programmer.connect_wifi, args=(self.add_text_log, output)).start()