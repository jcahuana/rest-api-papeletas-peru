from selenium import webdriver
import chromedriver_autoinstaller
from PIL import Image
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import sys
import os
from base64 import b64encode
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from classes.AntiCaptcha import Captcha

chromedriver_autoinstaller.install()


opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36')

browser = webdriver.Chrome(chrome_options=opts)

url = 'https://scppp.mtc.gob.pe'
browser.get(url)

try:
    dni = open("./private/dni.txt").readline().strip()
    injectDNI = 'document.getElementById("txtNroDocumento").value="' + \
        dni + '";'
    browser.execute_script(injectDNI)

    # Get captcha
    sleep(1)
    captcha_image = "./images/captcha.png"
    captachBox = browser.find_element(By.ID, "imgCaptcha")
    location = captachBox.location
    size = captachBox.size
    browser.save_screenshot("./images/screenshoot.png")

    x = location['x']
    y = location['y']
    w = size['width'] - 30
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open('./images/screenshoot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(captcha_image)

    captchaResolver = Captcha('./images/captcha.png')
    captchaCode = captchaResolver.getCode()

    """ headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    } """
    # request = requests.get("https://scppp.mtc.gob.pe/", headers=headers)

    injectCaptcha = 'document.getElementById("txtCaptcha").value="' + \
        captchaCode + '";'

    # Ejecuto los scripts con selenium
    browser.execute_script(injectCaptcha)

    submit_button = browser.find_element(
        by=By.XPATH, value='//a[@id="ibtnBusqNroDoc"]')
    submit_button.click()

    # Extraigo la informacion detras del captcha
    sleep(1)
    try:
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        registros = soup.find_all("tr", attrs={"class": "gridItemGroup"})
        data = []
        
        for registro in registros:
            data.append({
                "entidad": registro.select_one("td:nth-of-type(2)").text.replace(u'\xa0', u' '),
                "papeleta": registro.select_one("td:nth-of-type(3)").text.replace(u'\xa0', u' '),
                "fecha": registro.select_one("td:nth-of-type(4)").text.replace(u'\xa0', u' '),
                "fechaFirme": registro.select_one("td:nth-of-type(5)").text.replace(u'\xa0', u' '),
                "falta": registro.select_one("td:nth-of-type(6)").text.replace(u'\xa0', u' '),
                "estadoDeuda": registro.select_one("td:nth-of-type(7)").text.replace(u'\xa0', u' '),
                "resolucion": registro.select_one("td:nth-of-type(8)").text.replace(u'\xa0', u' '),
                "telefonoEntidad": registro.select_one("td:nth-of-type(9)").text.replace(u'\xa0', u' '),
                "retencionLicencia": registro.select_one("td:nth-of-type(10)").text.replace(u'\xa0', u' '),
            })
            
        print(data)
        
    except Exception as error:
        print("No se encontraron papeletas activas")

except Exception as e:

    print(e)
