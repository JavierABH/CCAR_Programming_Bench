import subprocess
import threading
import queue
import configparser

ini_path = r'C:\CCAR_Programming_Bench\__settings__\settings.ini'
config = configparser.ConfigParser()
config.read(ini_path)
config_section = config['Config']

def connect_usb(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy\\fw && '
        'adb kill-server && '
        'adb start-server'
    )
    execute_command(command, update_gui_callback, final_callback)

def connect_wifi(update_gui_callback, final_callback):
    ip = config['Config']['ip']
    command = (
        'cd /d C:\\scrcpy\\fw && '
        'adb kill-server && '
        f'adb connect {ip}:5555'
    )
    execute_command(command, update_gui_callback, final_callback)

def prog_android(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy\\fw && '
        'uuu_imx_android_flash.bat -f imx8mm -a -e -u ddr4 -d ddr4'
    )
    execute_command(command, update_gui_callback, final_callback)

def prog_stm_stlink(update_gui_callback, final_callback):
    program_path = r'C:\Program Files (x86)\STMicroelectronics\st_toolset\stvp\STVP_CmdLine.exe'
    bootloader_path = r'C:\scrcpy\stm\MCU_FW_Bootloader_concatenated_V_8.s19'

    command = f'"{program_path}" -BoardName=ST-LINK -Port=USB -ProgMode=SWIM -Device=STM8AF528 -Tool_ID=0 -verif -no_loop -no_log -progress -verbose -FileProg={bootloader_path}'
    execute_command(command, update_gui_callback, final_callback)

def prog_gps(update_gui_callback, final_callback):
    gps_path = config['Config']['GPS_file']
    command = (
        'cd /d C:\\scrcpy && '
        'adb root && '
        f'adb push {gps_path} /data/ClubCar/Download &&'
        'echo Execute gps update, wait to finish for the log && '
        'adb shell "cd vendor/bin && stop gpsd && gps_firmware /dev/ttymxc1 115200 0 /data/ClubCar/Download/V50_120_N115_0104.bin"'
    )
    execute_command(command, update_gui_callback, final_callback)

def prog_modem(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy && '
        'adb root && '
        'echo Execute modem update, wait to finish for the log && '
        'adb shell "cd data && stop vendor.ril.telit-daemon && telit_modem_config update"'
    )
    execute_command(command, update_gui_callback, final_callback)

def check_android(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy && '
        'adb shell getprop ro.build.software_version'
    )
    execute_command(command, update_gui_callback, final_callback)

def check_stm(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy && '
        'adb shell getprop persist.build.stm_fw_version'
    )
    execute_command(command, update_gui_callback, final_callback)

def check_gps(update_gui_callback, final_callback): 
    command = (
        'cd /d C:\\scrcpy && '
        'adb shell getprop persist.sys.gps_fw_version'
    )
    execute_command(command, update_gui_callback, final_callback)

def check_modem(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy && '
        'adb shell getprop vendor.telit.modem.config.status'
    )
    execute_command(command, update_gui_callback, final_callback)

def gereric_command(update_gui_callback, final_callback):
    command = (
        'cd /d C:\\scrcpy && '
        ''
    )
    execute_command(command, update_gui_callback, final_callback)

def enqueue_output(src, out, q):
    for line in iter(out.readline, ''):
        q.put(line)
    out.close()

def execute_command(command, update_gui_callback, final_callback):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    q_stdout = queue.Queue()
    q_stderr = queue.Queue()

    stdout_thread = threading.Thread(target=enqueue_output, args=('stdout', process.stdout, q_stdout))
    stderr_thread = threading.Thread(target=enqueue_output, args=('stderr', process.stderr, q_stderr))

    stdout_thread.daemon = True
    stderr_thread.daemon = True

    stdout_thread.start()
    stderr_thread.start()

    output = []

    def check_queues():
        nonlocal output
        while not q_stdout.empty():
            line = q_stdout.get_nowait()
            update_gui_callback(line)
            output.append(line)
        
        while not q_stderr.empty():
            line = q_stderr.get_nowait()
            update_gui_callback(line)
            output.append(line)

        if process.poll() is None:
            threading.Timer(0.1, check_queues).start()
        else:
            while not q_stdout.empty():
                line = q_stdout.get_nowait()
                update_gui_callback(line)
                output.append(line)

            while not q_stderr.empty():
                line = q_stderr.get_nowait()
                update_gui_callback(line)
                output.append(line)

            # Final output
            final_callback("".join(output))
    
    check_queues()