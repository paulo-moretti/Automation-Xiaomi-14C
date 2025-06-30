import time
import random
import os
import signal
import subprocess
import selenium.common
from selenium.common.exceptions import TimeoutException
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cmd_process = None

def execute_main_code():
    subprocess.Popen("start cmd /k python extrator_de_registro_de_servidor.py", shell=True)

def close_cmd():
    global cmd_process
    if cmd_process is not None:
        os.kill(cmd_process.pid, signal.SIGTERM) 
        cmd_process = None


def print_green(text):
    print("\033[92m {}\033[00m".format(text))

from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.set_capability("platformName", "Android")
options.set_capability("deviceName", "Redmi 14C")
options.set_capability("platformVersion", "15")
options.set_capability("appPackage", "br.gov.sp.prodesp.sousp")
options.set_capability("appActivity", "br.gov.sp.sousp.feature.splash.SplashActivity")
options.set_capability("automationName", "UiAutomator2")
options.set_capability("noReset", True)
options.set_capability("newCommandTimeout", 1000)

driver = None

def rolar_para_baixo(driver, duracao=400):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela['width']
    altura = tamanho_tela['height']
    x = largura // 2
    y_inicio = int(altura * 0.6)
    y_fim = int(altura * 0.4)
    driver.swipe(x, y_inicio, x, y_fim, duracao)
    time.sleep(0.7)  # Tempo para os meses carregarem

def rolar_para_cima_meses(driver, start_y_ratio=0.65, end_y_ratio=0.7, duration=600):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela['width']
    altura = tamanho_tela['height']
    x = largura // 2
    start_y = int(altura * start_y_ratio)
    end_y = int(altura * end_y_ratio)
    driver.swipe(x, start_y, x, end_y, duration)

def rolar_para_cima_anos(driver, start_y_ratio=0.5, end_y_ratio=0.55, duration=550):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela['width']
    altura = tamanho_tela['height']
    x = largura // 2
    start_y = int(altura * start_y_ratio)
    end_y = int(altura * end_y_ratio)
    driver.swipe(x, start_y, x, end_y, duration)

def capturar_elementos_incrementalmente(driver, resource_id, elementos_processados=None):
    if elementos_processados is None:
        elementos_processados = []

    novos_elementos = []

    while True:
        elementos_visiveis = driver.find_elements(AppiumBy.ID, resource_id)
        novos_elementos = [
            el.text.strip() for el in elementos_visiveis
            if el.text.strip() and el.text.strip() not in elementos_processados
        ]

        if not novos_elementos:
            break  # Nada novo, parar

        elementos_processados.extend(novos_elementos)
        print(f"Capturados até agora ({resource_id}): {elementos_processados}")

        rolar_para_baixo(driver)
    
    return elementos_processados

try:
    print_green("Conectando ao servidor Appium e iniciando o aplicativo...")
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', options=options)

    print_green("Abrindo o aplicativo e navegando até a tela de login...")

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/login")))
        driver.find_element(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/login").click()
        print_green("Botão 'Entrar com o gov.br' clicado com sucesso!")

        login_sucesso = False
        while not login_sucesso:
            usuario = input("Digite o seu CPF: ")
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
            )
            element.send_keys(usuario)
            driver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.widget.Button").click()

            senha = input("Digite a sua senha: ")
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.EditText"))
            )
            element.send_keys(senha)
            driver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.Button[3]").click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
                )
                print("Login falhou. Por favor, verifique o CPF e a senha e tente novamente.")
            except TimeoutException:
                login_sucesso = True
                print_green("Login realizado com sucesso!")

        try:
            botao_skip = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/bt_skip"))
            )
            botao_skip.click()
            print("Botão 'bt_skip' encontrado e clicado com sucesso.")
        except TimeoutException:
            print("Botão 'bt_skip' não encontrado. Continuando execução...")

    except TimeoutException:
        print("Elemento de login não encontrado. Verificando se o usuário já está logado...")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/iv_right"))
            )
            print_green("Usuário já está logado. Continuando execução...")
        except TimeoutException:
            print("Elemento de login e o indicador de usuário logado não foram encontrados. Verifique o estado do aplicativo.")
    
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/iv_right"))).click()
        print_green("Navegando até 'Demonstrativos de Pagamentos'...")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_cargo")))
        elementos = driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_cargo")
        textos_elementos = [el.text for el in elementos]

        if elementos:
            print("\nForam encontrados os seguintes elementos:")
            for i, texto in enumerate(textos_elementos, start=1):
                print(f"{i}° {texto}")

            escolha = int(input("\nDigite o número do elemento que você deseja selecionar: "))
            if 1 <= escolha <= len(elementos):
                elementos[escolha - 1].click()
                print_green(f"Elemento '{textos_elementos[escolha - 1]}' selecionado com sucesso!")
            else:
                print("Número inválido. Nenhum elemento foi selecionado.")
        else:
            print("Nenhum elemento foi encontrado na tela.")
    except TimeoutException:
        print("O tempo de espera para encontrar os elementos foi excedido.")

    WebDriverWait(driver, 60).until(
        lambda d: len(d.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/card")) > 1
    )
    driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/card")[0].click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.LinearLayout[@content-desc='ANTERIORES']"))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_info"))
    )

    print("Capturando todos os anos disponíveis de forma incremental...")
    anos_processados = []
    anos_textos = capturar_elementos_incrementalmente(driver, "br.gov.sp.prodesp.sousp:id/tv_info", anos_processados)
    anos_textos = [int(ano) for ano in anos_textos if ano.isdigit() and int(ano) > 1999]
    anos_textos.sort()
    print("Anos coletados:", anos_textos)

    for ano in anos_textos:
        print_green(f"Coletando ano {ano}")

        ano_encontrado = False
        elementos_visiveis = driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_info")
        for el in elementos_visiveis:
            if el.text.strip() == str(ano):
                try:
                    el.click()
                    print(f"Selecionado o ano {ano} com sucesso.")
                    ano_encontrado = True
                    break
                except Exception as e:
                    print(f"Erro ao clicar no ano {ano}: {e}")
                    break

        primeira_rolagem = True

        try:
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_data")))
            print("Capturando todos os meses disponíveis de forma incremental...")
            meses_processados = []
            meses_disponiveis = capturar_elementos_incrementalmente(driver, "br.gov.sp.prodesp.sousp:id/tv_data", meses_processados)

            if primeira_rolagem:
                rolar_para_baixo(driver)
                primeira_rolagem = False

            for i in range(len(meses_disponiveis) - 1, -1, -1):
                mes = meses_disponiveis[i]
                mes_encontrado = False

                for tentativa in range(10):  
                    elementos_visiveis = driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_data")

                    for el in elementos_visiveis:
                        if el.text.strip() == mes:
                            try:
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(el))
                                el.click()
                                print(f"Coletando mês {mes} do ano {ano}")
                                mes_encontrado = True
                                break
                            except Exception as e:
                                print(f"Erro ao clicar no mês {mes}: {e}")

                    if mes_encontrado:
                        break

                    rolar_para_cima_meses(driver)  # sobe um pouco a tela
                    time.sleep(0.7)  # tempo para elementos carregarem

                if not mes_encontrado:
                    print(f"Não foi possível clicar no mês {mes}. Pulando.")
                    continue

                # Botão Salvar
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/bt_save"))
                    ).click()
                    print("Botão 'Salvar' clicado com sucesso.")
                except TimeoutException:
                    print("Botão 'Salvar' não encontrado.")
                    continue

                # Botão de confirmação
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[contains(@text, "Salvar")]'))
                    ).click()
                    print("Botão de confirmação clicado com sucesso.")
                except TimeoutException:
                    print(" Botão de confirmação não encontrado. Prosseguindo.")
                    continue

                # Voltar
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Navegar para cima']"))
                    ).click()
                    print("Botão 'Voltar' clicado com sucesso.")
                except TimeoutException:
                    print("Botão 'Voltar' não encontrado.")
                    continue

                meses_processados.append(mes)
                time.sleep(1)

            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_ano"))
                ).click()
                rolar_para_cima_anos(driver)
                print("Voltando para a lista de anos.")
            except TimeoutException:
                print("Erro: Não foi possível voltar para a lista de anos. Verifique manualmente.")
        except TimeoutException:
            print("O tempo de espera para encontrar os elementos foi excedido.")
        except Exception as e:
            print(f"Erro ao capturar os meses: {e}")

finally:
    if driver is not None:
        driver.quit()

if __name__ == "__main__":
    print("Executando o código principal...")
    time.sleep(60) 
    print("Código principal finalizado.")
