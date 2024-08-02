import os
import subprocess
import threading
import queue

def prog_android():
    os.chdir(r"C:\scrcpy\FW")

    def enqueue_output(src, out, queue):
        for line in iter(out.readline, ''):
            queue.put(line)
        out.close()

    process = subprocess.Popen("uuu_imx_android_flash.bat -f imx8mm -a -e -u ddr4 -d ddr4",
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    q_stdout = queue.Queue()
    q_stderr = queue.Queue()

    stdout_thread = threading.Thread(target=enqueue_output, args=('stdout', process.stdout, q_stdout))
    stderr_thread = threading.Thread(target=enqueue_output, args=('stderr', process.stderr, q_stderr))

    stdout_thread.daemon = True
    stderr_thread.daemon = True

    stdout_thread.start()
    stderr_thread.start()

    output = ""
    
    while process.poll() is None:
        while not q_stdout.empty():
            line = q_stdout.get_nowait()
            print(line, end='')
            output += line  # agregar la línea a la variable de salida

        while not q_stderr.empty():
            line = q_stderr.get_nowait()
            print(line, end='')
            output += line  # agregar la línea a la variable de salida

    # Imprimir cualquier salida restante después de que el proceso haya finalizado
    while not q_stdout.empty():
        line = q_stdout.get_nowait()
        print("1" + q_stdout.get_nowait(), end='')
        line = q_stdout.get_nowait()

    while not q_stderr.empty():
        line = q_stderr.get_nowait()
        print(line, end='')
        output += line  # agregar la línea a la variable de salida
    
    # buscar en la variable de salida
    if "Start Cmd:FB: done" in output:
        return True
    else:
        return False