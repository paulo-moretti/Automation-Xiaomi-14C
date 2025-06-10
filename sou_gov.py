import time
import random
import os
import signal
import subprocess
import selenium.common
import json # Adicionado para manipulação de JSON
from selenium.common.exceptions import TimeoutException
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cmd_process = None

PROGRESS_FILE = 'automation_progress.json'

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'last_year': None, 'last_month': None}

def save_progress(year, month):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'last_year': year, 'last_month': month}, f)

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
options.set_capability("platformVersion", "14")
options.set_capability("appPackage", "br.gov.sp.prodesp.sousp")
options.set_capability("appActivity", "br.gov.sp.sousp.feature.splash.SplashActivity")
options.set_capability("automationName", "UiAutomator2")
options.set_capability("noReset", True)
options.set_capability("newCommandTimeout", 300)

driver = None

def rolar_para_baixo(driver, duracao=1000):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela["width"]
    altura = tamanho_tela["height"]
    x = largura // 3
    y_inicio = int(altura * 1.0)
    y_fim = int(altura * 0.5)
    driver.swipe(x, y_inicio, x, y_fim, duracao)

def rolar_para_cima_meses(driver, start_y_ratio=0.80, end_y_ratio=0.90, duration=1000):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela["width"]
    altura = tamanho_tela["height"]
    x = largura // 3
    start_y = int(altura * start_y_ratio)
    end_y = int(altura * end_y_ratio)
    driver.swipe(x, start_y, x, end_y, duration)

def rolar_para_cima_anos(driver, start_y_ratio=0.8, end_y_ratio=0.90, duration=1000):
    tamanho_tela = driver.get_window_size()
    largura = tamanho_tela["width"]
    altura = tamanho_tela["height"]
    x = largura // 3
    start_y = int(altura * start_y_ratio)
    end_y = int(altura * end_y_ratio)
    driver.swipe(x, start_y, x, end_y, duration)

def capturar_elementos_incrementalmente(driver, resource_id, elementos_processados=None):
    if elementos_processados is None:
        elementos_processados = []

    # Capturar elementos visíveis inicialmente
    elementos_visiveis = driver.find_elements(AppiumBy.ID, resource_id)
    novos_elementos = [el.text.strip() for el in elementos_visiveis if el.text.strip() and el.text.strip() not in elementos_processados]

    while novos_elementos:
        # Adicionar novos elementos ao conjunto processado
        elementos_processados.extend(novos_elementos)
        print(f"Capturados até agora ({resource_id}): {elementos_processados}")

        # Verificar se o elemento "2000" está entre os elementos processados
        if "2000" in novos_elementos:
            print("Elemento \'2000\' encontrado. Parando a função.")
            break

        # Rolar para baixo para encontrar mais elementos
        rolar_para_baixo(driver)
        time.sleep(2)

        # Atualizar os elementos visíveis e identificar novos
        elementos_visiveis = driver.find_elements(AppiumBy.ID, resource_id)
        novos_elementos = [el.text.strip() for el in elementos_visiveis if el.text.strip() and el.text.strip() not in elementos_processados]

    return elementos_processados

try:
    print_green("Conectando ao servidor Appium e iniciando o aplicativo...")
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', options=options)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/login")))

    print_green("Abrindo o aplicativo e navegando até a tela de login...")

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/login"))).click()
        print_green("Botão \'Entrar com o gov.br\' clicado com sucesso!")

        login_sucesso = False
        while not login_sucesso:
            usuario = input("Digite o seu CPF: ")
            # Campo CPF - Usando XPATH fornecido pelo usuário (mantido do Redmi 14C)
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
            )
            element.send_keys(usuario)
            # Botão Continuar - Usando XPATH fornecido pelo usuário (mantido do Redmi 14C)
            driver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View[3]/android.widget.Button").click()

            senha = input("Digite a sua senha: ")
            # Campo Senha - Usando XPATH fornecido pelo usuário (mantido do Redmi 14C)
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.EditText"))
            )
            element.send_keys(senha)
            # Botão Entrar - Usando XPATH fornecido pelo usuário (mantido do Redmi 14C)
            driver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View[3]/android.view.View/android.view.View[1]/android.widget.Button[3]").click()

            try:
                # Verificando se voltou para a tela de CPF (login falhou) (mantido do Redmi 14C)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
                )
                print("Login falhou. Por favor, verifique o CPF e a senha e tente novamente.")
            except TimeoutException:
                login_sucesso = True
                print_green("Login realizado com sucesso!")

        try:
            # Botão Pular Tutorial - Usando ID fornecido pelo usuário (mantido do Redmi 14C)
            botao_skip = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/bt_skip"))
            )
            botao_skip.click()
            print("Botão \'bt_skip\' encontrado e clicado com sucesso!")
        except TimeoutException:
            print("Botão \'bt_skip\' não encontrado. Continuando execução...")

    except TimeoutException:
        print("Elemento de login não encontrado. Verificando se o usuário já está logado...")
        try:
            # Elemento após login - Usando ID fornecido pelo usuário (mantido do Redmi 14C)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/iv_right"))
            )
            print_green("Usuário já está logado. Continuando execução...")
        except TimeoutException:
            print("Elemento de login e o indicador de usuário logado não foram encontrados. Verifique o estado do aplicativo.")

    # Elemento clicado após login - Usando ID fornecido pelo usuário (mantido do Redmi 14C)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/iv_right"))).click()
    print_green("Navegando até \'Demonstrativos de Pagamentos\'...")

    try:
        # Elementos de seleção de vínculo - Usando ID fornecido pelo usuário (tv_cargo) (mantido do Redmi 14C)
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_cargo"))
        )
        elementos = driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_cargo")
        textos_elementos = [el.text for el in elementos]

        if elementos:
            print("\nForam encontrados os seguintes elementos:")
            for i, texto in enumerate(textos_elementos, start=1):
                print(f"{i}° {texto}")

            escolha = int(input("\nDigite o número do elemento que você deseja selecionar: "))
            if 1 <= escolha <= len(elementos):
                elementos[escolha - 1].click()
                print_green(f"Elemento \'{textos_elementos[escolha - 1]}\' selecionado com sucesso!")
            else:
                print("Número inválido. Nenhum elemento foi selecionado.")
        else:
            print("Nenhum elemento foi encontrado na tela.")
    except TimeoutException:
        print("O tempo de espera para encontrar os elementos foi excedido.")

    # Elementos demonstrativos - O script original usava card, mas não foi fornecido um locator específico para o Redmi 14C.
    # Mantendo o locator original por enquanto, mas pode precisar de ajuste se não funcionar.
    WebDriverWait(driver, 60).until(
        lambda d: len(d.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/card")) > 1
    )
    driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/card")[0].click()

    # Aba ANTERIORES - Usando XPATH (mantido do Redmi 14C)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.LinearLayout[@content-desc=\'ANTERIORES\']"))
    ).click()

    # Elementos dos anos - Usando ID (mantido do Redmi 14C)
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_info"))
    )

    print("Capturando todos os anos disponíveis de forma incremental...")
    anos_processados = []
    # Usando ID para capturar anos
    anos_textos = capturar_elementos_incrementalmente(driver, "br.gov.sp.prodesp.sousp:id/tv_info", anos_processados)
    anos_textos = [int(ano) for ano in anos_textos if ano.isdigit() and int(ano) > 1999]
    anos_textos.sort()
    print("Anos coletados:", anos_textos)

    # Carregar progresso (ADICIONADO DO S10+)
    progress = load_progress()
    start_year = progress['last_year']
    start_month = progress['last_month']

    for ano in anos_textos:
        if start_year and ano < start_year:
            print(f"Pulando ano {ano} (já processado anteriormente).")
            continue

        print_green(f"Coletando ano {ano}")

        ano_encontrado = False
        # Usando ID para encontrar elementos de ano (mantido do Redmi 14C)
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

        if not ano_encontrado:
            print(f"Ano {ano} não encontrado na tela. Tentando rolar para encontrar.")
            # Implementar lógica de rolagem para encontrar o ano, se necessário
            # Por enquanto, vamos assumir que todos os anos estão visíveis ou que a rolagem já é tratada por capturar_elementos_incrementalmente
            continue

        primeira_rolagem = True

        try:
            # Elementos dos meses - Usando ID (mantido do Redmi 14C)
            WebDriverWait(driver, 70).until(
                EC.presence_of_all_elements_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_data"))
            )
            print("Capturando todos os meses disponíveis de forma incremental...")
            meses_processados = []
            # Usando ID para capturar meses
            meses_disponiveis = capturar_elementos_incrementalmente(driver, "br.gov.sp.prodesp.sousp:id/tv_data", meses_processados)

            if primeira_rolagem:
                rolar_para_baixo(driver)
                primeira_rolagem = False

            # Ajustar a iteração para começar do mês salvo (ADICIONADO DO S10+)
            start_index = 0
            if start_year == ano and start_month:
                try:
                    start_index = meses_disponiveis.index(start_month) + 1
                    print(f"Reiniciando do mês {start_month} (índice {start_index}).")
                except ValueError:
                    print(f"Mês {start_month} não encontrado na lista de meses disponíveis para o ano {ano}. Começando do início.")

            for i in range(len(meses_disponiveis) - 1, start_index - 1, -1):
                mes = meses_disponiveis[i]

                # Se o mês já foi processado no ano atual, pular (ADICIONADO DO S10+)
                if start_year == ano and start_month and i < meses_disponiveis.index(start_month):
                    print(f"Pulando mês {mes} do ano {ano} (já processado anteriormente).")
                    continue

                elementos_visiveis = driver.find_elements(AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/tv_data")
                mes_encontrado = False
                for el in elementos_visiveis:
                    if el.text.strip() == mes:
                        try:
                            WebDriverWait(driver, 70).until(EC.element_to_be_clickable(el))
                            el.click()
                            print(f"Coletando mês {mes} do ano {ano}.")
                            mes_encontrado = True
                            break
                        except Exception as e:
                            print(f"Erro ao clicar no mês {mes} do ano {ano}: {e}")
                            continue

                if mes_encontrado:
                    try:
                        # Botão Salvar (inicial) - Usando ID (mantido do Redmi 14C)
                        WebDriverWait(driver, 70).until(
                            EC.presence_of_element_located((AppiumBy.ID, "br.gov.sp.prodesp.sousp:id/bt_save"))
                        ).click()
                        print("Botão \'Salvar\' clicado com sucesso!")
                    except TimeoutException:
                        print("Erro: Botão \'Salvar\' não foi encontrado. Pulando para o próximo mês.")
                        continue

                    # Adicionado: Interação com o botão \'Salvar\' na tela do Google Drive (ADICIONADO DO S10+)
                    try:
                        WebDriverWait(driver, 70).until(
                            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[contains(@text, "Salvar")]'))
                        ).click()
                        print("Botão \'Salvar\' do Google Drive clicado com sucesso!")
                    except TimeoutException:
                        print("Erro: Botão \'Salvar\' do Google Drive não foi encontrado.")
                        # Dependendo do fluxo, pode ser necessário adicionar um \'continue\' ou outro tratamento de erro aqui
                        pass # Mantendo a execução para os próximos meses, mas o salvamento falhou para este mês

                    # Salvar progresso após processar o mês com sucesso (ADICIONADO DO S10+)
                    save_progress(ano, mes)
                    print(f"Progresso salvo: Ano {ano}, Mês {mes}")

                    try:
                        # Botão Voltar - Usando XPATH (mantido do Redmi 14C)
                        WebDriverWait(driver, 70).until(
                            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc=\'Navegar para cima\']"))
                        ).click()
                        print("Botão \'Voltar\' clicado com sucesso!")
                        rolar_para_cima_meses(driver)

                    except TimeoutException:
                        print("Erro: Botão de navegação \'Voltar\' não foi encontrado. Tentando prosseguir.")
                        continue

                    meses_processados.append(mes)
                    time.sleep(1)

            # Limpar progresso do mês após todos os meses do ano serem processados (ADICIONADO DO S10+)
            save_progress(ano, None)
            print(f"Todos os meses do ano {ano} processados. Limpando progresso do mês.")

            try:
                # Elemento para voltar para a lista de anos (mantido do Redmi 14C)
                WebDriverWait(driver, 70).until(
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
    time.sleep(40)
    print("Automação finalizada.")

