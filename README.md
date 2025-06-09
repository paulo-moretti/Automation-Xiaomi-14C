# Automação Android

Este projeto realiza a automação de interações com aplicativos Android utilizando **Python** e **Appium**, permitindo a execução de tarefas repetitivas de maneira eficiente. A solução foi projetada para gerenciar processos auxiliares, como o servidor Appium, e automatizar operações no aplicativo **SouGov**, incluindo login, navegação e coleta de dados.

## Estrutura do Projeto

O projeto é composto pelos seguintes scripts:

1. **`start.py`**:
 - Gerencia a inicialização dos serviços necessários, como o servidor Appium e o script principal de automação (`sou_gov.py`).
 - Finaliza processos ao término da execução.

2. **`process.py`**:
 - Inicia o servidor Appium em um terminal separado, utilizando comandos do sistema operacional.

3. **`sou_gov.py`**:
   - Script principal que realiza a automação do aplicativo SouGov.
   - Implementa login automatizado, navegação por menus, rolagem e coleta de informações.

## Requisitos

### Software Necessário

Certifique-se de instalar os seguintes componentes:

- **Python 3.x** e gerenciador de pacotes `pip`.
- **Node.js** (necessário para o Appium):
  ```bash
  npm install -g appium`` 

-   **Appium Server** (instalado via `npm`).
-   **Java JDK** (8 ou superior).
-   **Android SDK Tools**, incluindo:
    -   `platform-tools` (para utilizar o comando `adb`).
-   **Google Chrome** no dispositivo Android e o respectivo `chromedriver`.

### Dependências do Python

Instale as dependências Python com o seguinte comando:

`pip install appium selenium` 

### Configurações do Ambiente

Adicione os seguintes caminhos à variável de ambiente `PATH`:

1.  **Node.js**: Diretório de instalação.
2.  **Java JDK**: Inclua o caminho para a pasta `bin` do JDK.
3.  **Android SDK Tools**: Caminhos para `platform-tools` e `tools`.
4.  **Python**: Diretório de instalação.
5.  **Chromedriver**: Diretório onde está localizado o executável do `chromedriver`.
6.  **System32 (Windows)**: Adicione o caminho `C:\Windows\System32`.

### Configuração do `chromedriver`

Baixe a versão do `chromedriver` compatível com a versão do Google Chrome instalada no dispositivo Android. Atualize o caminho no script `sou_gov.py`:


`options.set_capability("chromedriverExecutable", "C:/caminho/do/chromedriver.exe")` 

### Verificando a Conexão com o Dispositivo

Ative a depuração USB no dispositivo Android e conecte-o ao computador. Confirme a conexão com o comando:

`adb devices` 

Se o dispositivo aparecer na lista, ele está pronto para uso.

## Como Usar

### Passo 1: Preparação

1.  Conecte o dispositivo Android ao computador via USB (Ative a depuração USB).
2.  Certifique-se de que o servidor Appium está instalado e configurado corretamente.

### Passo 2: Execução do Projeto

1.  Inicie o script principal com o comando:
    
    `python start.py` 
    
    Esse script:
    
    -   Inicializa o servidor Appium (`process.py`).
    -   Executa o script principal de automação (`sou_gov.py`).
2.  Durante a execução, insira as credenciais do SouGov (CPF e senha) quando solicitado.
    

### Passo 3: Monitoramento

-   Acompanhe o terminal para verificar mensagens de progresso e identificar possíveis erros.
-   O script realizará automaticamente as tarefas programadas, como login e coleta de dados.

### Finalização

-   O script encerrará automaticamente os processos ao término da execução.

## Personalização

1.  **Dispositivo Android**: Atualize os detalhes do dispositivo no script `sou_gov.py`:
    
    
    `options.set_capability("deviceName", "Galaxy S10+")
    options.set_capability("platformVersion", "12.0")` 
    
2.  **Elementos da Interface**: Personalize os identificadores e os fluxos de interação com o aplicativo conforme necessário.
    

## Solução de Problemas

1.  **Erro de Conexão com o Appium**:
    
    -   Certifique-se de que o servidor Appium está em execução.
    -   Verifique se a porta padrão (`4723`) está disponível.
 
2.  **Dispositivo Não Reconhecido**:
    
    -   Garanta que a depuração USB esteja habilitada no dispositivo.
    -   Verifique se o `adb` reconhece o dispositivo com o comando:
        
        
        `adb devices` 
        
3.  **Erro no `chromedriver`**:
    
    -   Verifique a compatibilidade entre o `chromedriver` e a versão do Google Chrome instalada no dispositivo.


## Contribuição

- Faça um fork do projeto.
- Crie um branch para sua nova feature (git checkout -b nova-feature).
- Commit suas mudanças (git commit -m 'Adiciona nova feature').
- Faça o push para o branch (git push origin nova-feature).
- Abra um pull request.

# Licença de Uso 

Este software foi desenvolvido por Paulo Eduardo Moretti. Ao utilizar, modificar ou distribuir este software, você concorda com os seguintes termos:

## Permissões

- **Uso pessoal**: Você pode utilizar este software para uso pessoal e projetos próprios.
- **Modificações**: Você pode modificar o código-fonte para adaptar o software às suas necessidades, desde que as modificações sejam mantidas em caráter privado ou interno.
- **Distribuição**: Você pode distribuir o software original ou modificado, desde que mantenha esta licença incluída em todas as cópias distribuídas.

## Restrições

- **Uso comercial**: O uso deste software para fins comerciais é **proibido** sem a permissão explícita e por escrito do autor.
- **Garantias**: Este software é fornecido "como está", sem garantias de qualquer tipo. O autor não se responsabiliza por quaisquer danos ou problemas causados pela utilização deste software.
- **Atribuição**: Ao utilizar ou distribuir este software, você deve fornecer a devida atribuição ao autor original, Paulo Eduardo Moretti.

## Limitação de Responsabilidade

Em nenhuma hipótese o autor será responsável por qualquer dano direto, indireto, incidental, especial, exemplar ou consequente (incluindo, mas não se limitando a, aquisição de bens ou serviços substitutos; perda de uso, dados ou lucros; ou interrupção de negócios) decorrente de qualquer forma do uso deste software, mesmo que advertido da possibilidade de tais danos.

## Alterações e Revogação

O autor reserva-se o direito de alterar esta licença a qualquer momento, sem aviso prévio, desde que tal alteração seja devidamente registrada no repositório oficial do projeto. Esta licença poderá ser revogada a qualquer momento em caso de violação de quaisquer de seus termos.

---

© 2024 Paulo Eduardo Moretti. Todos os direitos reservados.
