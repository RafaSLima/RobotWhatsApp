#IMPORTAR AS BIBLIOTECAS

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pyodbc
import pyautogui


#CONECTANDO COM O BANCO

server = 'wocc60'
database = 'ITEMS_SHIP'
username = 'sa'
password = 'Winover@357'
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + 
';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = connection.cursor()

# NAVEGANDO ATE O WPP

options = webdriver.ChromeOptions()
options.add_argument('lang=pt-br')
options.add_argument('--start-maximized')
options.add_argument('--user-data-dir=C:\\Users\\rafael.lima\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
options.add_argument('--profile-directory=Profile 1')

cursor.execute("SELECT ID FROM SEND_WHATSAPP WHERE VALIDATTION = 0 ORDER BY DATE_PROC")
ids = cursor.fetchall()

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
driver.get('https://web.whatsapp.com/')
time.sleep(10)


def navegation(contact):

    search = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    search.send_keys(contact)
    time.sleep(3)

    party = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]')
    party.click()
    time.sleep(3)



def send_message(message):

    msg = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
    msg.send_keys(message)
    time.sleep(3)

    send = driver.find_element_by_class_name('_4sWnG')
    send.click()
    time.sleep(3)

def send_image(image):
    
    img = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[1]/div[2]/div/div/span')
    img.click()
    time.sleep(2)

    anexo = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button')
    anexo.click()
    time.sleep(5)

    pyautogui.typewrite(image)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)
    
    send_img = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span')
    send_img.click()
    time.sleep(8)

def send_file(file):
    
    doc = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[1]/div[2]/div/div/span')
    doc.click()
    time.sleep(2)

    doc_span = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[1]/div[2]/div/span/div[1]/div/ul/li[3]/button')
    doc_span.click()
    time.sleep(2)

    pyautogui.write(file)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(3)

    send_file = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span')
    send_file.click()
    time.sleep(8)

for id in ids:
    cursor.execute("SELECT CONTACT FROM SEND_WHATSAPP WHERE ID =?", id)
    contact = cursor.fetchall()
    cursor.execute("SELECT MESSAGE FROM SEND_WHATSAPP WHERE ID =?", id)
    message =cursor.fetchall()
    cursor.execute("SELECT SRC_IMG FROM SEND_WHATSAPP WHERE ID =?", id)
    img = cursor.fetchall()
    cursor.execute("SELECT SRC_FILE FROM SEND_WHATSAPP WHERE ID =?",id)
    file = cursor.fetchall()
    navegation(contact[0][0])
    if message[0][0] != None:
        send_message(message[0][0])
    if img[0][0] != None:
        send_image(img[0][0])
    if file[0][0] != None:
        send_file(file[0][0])
    cursor.execute("UPDATE SEND_WHATSAPP SET VALIDATTION = 1, DATE_SHIP = GETDATE() WHERE ID=?",id)
    cursor.commit()







driver.quit()