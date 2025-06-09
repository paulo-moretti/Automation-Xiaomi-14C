import subprocess

def start_appium():
    subprocess.Popen("start cmd /k appium", shell=True)

if __name__ == "__main__":
    print("Iniciando o Appium...")
    start_appium()
