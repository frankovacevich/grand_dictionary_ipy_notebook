import requests
from bs4 import BeautifulSoup
import datetime

def getHTMLCode(url, retry = 10):
    try:
        req = requests.get(url, timeout=30)
        req.encoding = 'utf-8' 
        print("Processing fetch ...")
        return BeautifulSoup(req.text, 'html.parser')
    except:
        raise
        if retry == 0:
            return ""
        
        print("Retrying ...")
        return getHTMLCode(url, retry - 1)



def remove_shit(text):
    text = text.lower()
    text = text.replace("<"," ")
    text = text.replace(">"," ")
    text = text.replace("•"," ")
    text = text.replace("[","")
    text = text.replace("]","")
    text = text.replace("{","")
    text = text.replace("}","")
    text = text.replace("(","")
    text = text.replace(")","")
    text = text.replace(".","")
    text = text.replace(",","")
    text = text.replace(";","")
    text = text.replace("-"," ")
    text = text.replace("?","")
    text = text.replace("!","")
    text = text.replace("1","")
    text = text.replace("2","")
    text = text.replace("3","")
    text = text.replace("4","")
    text = text.replace("5","")
    text = text.replace("6","")
    text = text.replace("7","")
    text = text.replace("8","")
    text = text.replace("9","")
    text = text.replace("0","")
    text = text.replace("'"," ")
    text = text.replace("«"," ")
    text = text.replace("»"," ")
    text = text.replace("„"," ")
    
    while "\n\n" in text:
        text = text.replace("\n\n","\n")
    
    return text


def log_(filename, text):
    if not filename.endswith(".log"):
        filename = filename + ".log"
    
    logfile = open(filename,"a+",encoding="UTF-8")
    logfile.write("> " + str(datetime.datetime.now()) + "  " + text + "\n")
    logfile.close()
    return

