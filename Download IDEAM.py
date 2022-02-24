"""
Created on Thu Apr 1 12:31:49 2021
@author: John Alexander Sandoval Barrera - UNAL
EDITED: Santiago Duarte - IHE Delft
"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd
from zipfile import ZipFile
import warnings
warnings.filterwarnings("ignore")

# def DHIME_Download(Path,DateIni,DateFin,Parameter,Variable,Department,Code,TimeWait=10):

# Ejemplo
Path="C:/Users/santi/Downloads/"
Parameter="PRECIPITACION"
Variable="PTPM_CON"
TimeWait=15



stations=pd.read_csv("Datos_Tolima.csv")
dates=["01/01/1980","01/01/1990","01/01/2000","01/01/2010","01/01/2020"]
all=pd.DataFrame(columns=stations["Codigo"],index=pd.date_range(start=dates[0], end=dates[-1]))

#for i in range(stations.shape[0]):
i=0
Department=stations["Dpto"][i]
Code=stations["Codigo"][i]




for j in range(0,3):
    DateIni=dates[j]
    DateFin=dates[j+1]
    # Abrir Google Chrome operado con Selenium cambiando la carpeta de descargas
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #, options=chrome_options
    # Abrir la página inicial del DHIME
    browser.get('http://dhime.ideam.gov.co/atencionciudadano/')
    #Aceptar los terminos y condiciones de la página
    try:
        button = WebDriverWait(browser, TimeWait*1.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".checkbox")))
    except:
        print("Tiempo de carga de la página superado, aumentar el valor de TimeWait")
        # return
    button.click()
    button = browser.find_element_by_css_selector(".enable-btn")
    button.click()
    #Introducir las fechas de inicio y final de la descarga
    Date_ini = WebDriverWait(browser, TimeWait*1.5).until(EC.presence_of_element_located((By.ID, "datepicker")))
    Date_ini.click()
    Date_ini.clear()
    Date_ini.send_keys(DateIni)
    Date_fin = browser.find_element_by_id("datepicker1")
    Date_fin.click()
    Date_fin.clear()
    Date_fin.send_keys(DateFin)
    #Seleccionar parametro a descargar
    Par = browser.find_element_by_xpath("//div[@id='pnlEstandar']/table/tbody/tr/td[2]/span/span/span")
    Par.click()
    Par2 = browser.find_element_by_xpath("//li[contains(.,'"+Parameter+"')]")
    Par2.click()
    # Seleccionar variable a descargar
    Var = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@onclick,'"+Variable+"')]")))
    Var.click()
    # Seleccionar departamento
    Dep = browser.find_element_by_xpath("//div[@id='first']/table/tbody/tr/td[2]/span/span/span")
    Dep.click()
    time.sleep(TimeWait/4)
    Dep_Index = int(WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//li[contains(.,'"+Department+"')]"))).get_attribute('outerHTML').split('"')[9]) + 1
    Dep2 = browser.find_element_by_xpath("//ul[@id='deptos2_listbox']/li["+str(Dep_Index)+"]")
    Dep2.click()
    # Seleccionar municipio (Todos)
    Mun = browser.find_element_by_xpath("//div[@id='first']/table/tbody/tr[2]/td[2]/span/span/span")
    Mun.click()
    Mun2 = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//ul[@id='municipio2_listbox']/li[2]")))
    Mun2.click()
    # Seleccionar estación
    Est_cod = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//input[@value='"+str(Code)+"']"))).get_attribute('outerHTML')
    Est_cod_sep = Est_cod.split()[1].replace('"',"").replace("id=idEstacionmetaData","")
    Est_cod_id = "//input[@id='checkMetaData"+Est_cod_sep+"']"
    Est = browser.find_element_by_xpath(Est_cod_id)
    Est.click()
    # Agregar a la consulta
    Search = browser.find_element_by_xpath("//div[@id='first']/div[5]/div")
    Search.click()
    #Iniciar descarga
    Download = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//div[@id='second']/div/div[3]/div")))
    Download.click()
    #Aceptar terminos de uso
    Accept = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.ID, "dijit_form_Button_2_label")))
    Accept.click()
    time.sleep(TimeWait*1.2)
    browser.close()
    # Extraer el archivo .csv del archivo comprimido descargado
    zf = ZipFile(Path+'/datos.zip', 'r')
    zf.extractall(Path)
    zf.close()
    # Cambiar el nombre del archivo extraido
    name=str(Code)+'-'+Variable+'-'+DateIni.replace('/','')+'-'+DateFin.replace('/','')+'.csv'
    os.rename(Path+'/excel.csv.csv', Path+'/'+name)
    # Eliminar el comprimido
    os.remove(Path+"/datos.zip")
    print(name+' Descargado')
    partial=pd.read_csv(Path+name)
    all[Code][pd.to_datetime(partial["Fecha"])]=partial["Valor"].values



# DHIME_Download(Path="C:/Users/fdu001/Downloads/",DateIni="01/01/1970", DateFin="01/01/1980", Parameter="PRECIPITACION", Variable="PTPM_CON", Department="Tolima", Code="22050080")




