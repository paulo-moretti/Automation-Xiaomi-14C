import subprocess
import time
import sys
import os

def start_process(script):
    # Determina o caminho correto do script
    if getattr(sys, 'frozen', False):  # Verifica se está rodando como executável
        base_path = sys._MEIPASS  # Diretório temporário onde o PyInstaller extrai os arquivos
        script_path = os.path.join(base_path, script)
    else:  # Durante o desenvolvimento
        script_path = script

    # Chama o script diretamente
    return subprocess.Popen(f"python {script_path}", shell=True)

def close_process_by_name(process_name):
    try:
        result = subprocess.check_output("tasklist", shell=True, text=True)
        for line in result.splitlines():
            if process_name in line:
                pid = int(line.split()[1]) 
                subprocess.call(f"taskkill /PID {pid} /F", shell=True)
                print(f"Processo {process_name} encerrado com sucesso.")
    except Exception as e:
        print(f"Erro ao encerrar o processo {process_name}: {e}")                                                     

if __name__ == "__main__":
    appium_process = start_process("process.py")

    try:
        sou_gov_process = start_process("sou_gov.py")

        sou_gov_process.wait()

    finally:
        print("Finalizando o Appium...")
        close_process_by_name("cmd.exe") 
        
        