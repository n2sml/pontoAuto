from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
from datetime import date
import calendar
import time
import random
import schedule

## Script utilizando Selenium para automatização da batida do ponto.
## Perceba que não cito o nome da empresa, nem o nome do sistema,
## tampouco meus dados :p

mainurl = ''
login = ''
senha = ''
codEmpresa = '1'

delay_carregar_tela = 3
delay_intervalo = 360
delay_final = 120

lista_dias_excecao = []

horario_inicio = '07:55'
horario_almoco_inicio = '11:55'
horario_almoco_fim = '12:55'
horario_fim = '16:55'

dir_salvar_imagem = r'C:\Registros\screenshot'

data_hoje = date.today()
nome_hoje = calendar.day_name[data_hoje.weekday()]

def chamar_timeout_random():
    print('     Rodando timeout: ')  
    num_random = random.randrange(0, delay_intervalo, 1)
    print("     " + str(num_random))
    time.sleep(num_random)        
    print('     Timeout concluido.')

def chamar_timeout_final():
    time.sleep(delay_final)
    

def printar_tela(nome): 
    print("     Datahora:" + nome)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(dir_salvar_imagem + nome + '.png')

def job_ponto():
    print('Iniciando job...')
    chamar_timeout_random()    

    print('Inicializando Webdriver')
    print('     Configurando Webdriver...')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})    

    driver = webdriver.Chrome(options = chrome_options)

    driver.set_window_size(1024, 600)
    driver.maximize_window()    
    print('     Pronto.')

    print('     Definindo url incial de acesso...')
    print('     ' + mainurl)
    driver.get(mainurl)

    print("     Preenchendo campos iniciais...")
    elemCod = driver.find_element(By.ID, 'CodEmpresa')
    elemCod.clear()
    elemCod.send_keys(codEmpresa)

    elemLogin = driver.find_element(By.ID, 'requiredusuario')
    elemLogin.clear()
    elemLogin.send_keys(login)

    elemSenha = driver.find_element(By.ID, 'requiredsenha')
    elemSenha.clear()
    elemSenha.send_keys(senha)

    elemSenha.send_keys(Keys.RETURN)
    print("     Campos preenchidos.")

    print("     Navegando em submenus...")
    elemLancamentos = WebDriverWait(driver, delay_carregar_tela).until(EC.presence_of_element_located((By.ID, 'menu2')))
    elemLancamentos = driver.find_element(By.ID, 'menu2')
    action = ActionChains(driver)
    action.move_to_element(elemLancamentos)
    action.perform()

    elemMarcacao = driver.find_element(By.CSS_SELECTOR, '#menu2_Item1 > a:nth-child(1)')
    elemMarcacao.click()
    print("     Pronto.")

    print("     Alternando janela...")
    janelaConfirmar = driver.window_handles[1]
    driver.switch_to.window(janelaConfirmar)
    print("     Janela alterada.")

    print("     Aguardando identificador...")
    elemDataPonto = WebDriverWait(driver, delay_carregar_tela).until(EC.presence_of_element_located((By.ID, 'data')))
    elemDataPonto = driver.find_element(By.ID, 'data')
    print("     Carregado.")

    print("     Colhendo informações...")
    dataPonto = elemDataPonto.get_attribute('value')

    elemHoraPonto = driver.find_element(By.CSS_SELECTOR,'input.CampoCentro:nth-child(4)')
    horaPonto = elemHoraPonto.get_attribute('value')
    print("     Informações coletadas com sucesso.")

    printar_tela(dataPonto.replace(r'/', '-') + '_' + horaPonto.replace(':', '-'))

    elemBotaoPonto = driver.find_element(By.ID,'Button1')
    elemBotaoPonto.click()

    chamar_timeout_final()

    print("Operação concluida com sucesso.")

# job_ponto()

print("Rodando agendadores...")
print("Segunda-feira...")
schedule.every().monday.at(horario_inicio).do(job_ponto)
schedule.every().monday.at(horario_almoco_inicio).do(job_ponto)
schedule.every().monday.at(horario_almoco_fim).do(job_ponto)
schedule.every().monday.at(horario_fim).do(job_ponto)
print("Segunda-feira ok")

print("Terça-feira...")
schedule.every().tuesday.at(horario_inicio).do(job_ponto)
schedule.every().tuesday.at(horario_almoco_inicio).do(job_ponto)
schedule.every().tuesday.at(horario_almoco_fim).do(job_ponto)
schedule.every().tuesday.at(horario_fim).do(job_ponto)
print("Terça-feira ok")    
    
print("Quarta-feira...")
schedule.every().wednesday.at(horario_inicio).do(job_ponto)
schedule.every().wednesday.at(horario_almoco_inicio).do(job_ponto)
schedule.every().wednesday.at(horario_almoco_fim).do(job_ponto)
schedule.every().wednesday.at(horario_fim).do(job_ponto)
print("Quarta-feira ok")

print("Quinta-feira...")
schedule.every().thursday.at(horario_inicio).do(job_ponto)
schedule.every().thursday.at(horario_almoco_inicio).do(job_ponto)
schedule.every().thursday.at(horario_almoco_fim).do(job_ponto)
schedule.every().thursday.at(horario_fim).do(job_ponto)
print("Quinta-feira ok") 

print("Sexta-feira...")
schedule.every().friday.at(horario_inicio).do(job_ponto)
schedule.every().friday.at(horario_almoco_inicio).do(job_ponto)
schedule.every().friday.at(horario_almoco_fim).do(job_ponto)
schedule.every().friday.at(horario_fim).do(job_ponto)
print("Sexta-feira ok") 

while True:
    schedule.run_pending()
    time.sleep(1)
