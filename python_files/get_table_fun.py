
def word_scheme(tables, name = "", type_ = "", ID = "", english = []):
    text = "<word>\n"
    text += "<ID>" + str(ID) + "</ID>\n"
    text += "<name>" + name + "</name>\n"
    text += "<type>" + type_ + "</type>\n"
    text += "<webpage>,,http://sh.wiktionary.org/wiki/" + name + "</webpage>\n"
    text += "<originaldef></originaldef>\n"
    text += "<synonyms></synonyms>\n"
    text += "<relatedwords></relatedwords>\n"
    text += "<english>\n"

    for en in english:
        text += "<en>" + en + "</en>\n"

    text += "</english>\n"
    text += "<examples>\n"
    text += "</examples>\n"
    text += tables.replace("<tb>Declension of </tb>","<tb>Declension of " + name + "</tb>")
    text += "</word>\n"
    return text

def AccomodateStringForFileWriting(string):
    string = string.replace("ȕ","u")
    string = string.replace("ū","u")
    string = string.replace("ú","u")
    string = string.replace("ù","u")
    
    string = string.replace("ē","e")
    string = string.replace("è","e")
    string = string.replace("ȅ","e")
    string = string.replace("é","e")
    
    string = string.replace("ī","i")
    string = string.replace("ì","i")
    string = string.replace("ȉ","i")
    string = string.replace("ȉ","i")
    string = string.replace("í","i")
    
    string = string.replace("ā","a")
    string = string.replace("à","a")
    string = string.replace("ȁ","a")
    string = string.replace("á","a")
    
    string = string.replace("ō","o")
    string = string.replace("ȍ","o")
    string = string.replace("ó","o")
    string = string.replace("ò","o")
    
    return string

def GET_ADJECTIVE(soup):
    tables = soup.find_all('table')
    r_tekst = "<tables>\n"

    table_name_adj = ["positive indefinite forms","positive definite forms","comparative forms", "superlative forms"]
    j = 0

    for table in tables:
        table_body = table.find('tbody')

        data = []
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])


        data.pop(0)
        data.pop(7)
        data = list(map(list, zip(*data)))
        text = "singular,nominative singular,genitive singular,dative singular,accusative (in./anim.) singular,vocative singular,locative singular,instrumental singular,nominative plural,genitive plural,dative plural,accusative plural,vocative plural,locative plural,instrumental plural"

        for i in range(0,3):
            if i == 0:
                text += ",,masculine"
            elif i == 1:
                text += ",,feminine"
            elif i == 2:
                text += ",,neuter"
            
            
            text += "," + data[i][0]
            text += "," + data[i][1]
            text += "," + data[i][2]
            text += "," + data[i][3]
            text += "," + data[i][4]
            text += "," + data[i][5]
            text += "," + data[i][6]
            text += "," + data[i][7]
            text += "," + data[i][8]
            text += "," + data[i][9]
            text += "," + data[i][10]
            text += "," + data[i][11]
            text += "," + data[i][12]
            text += "," + data[i][13]
            

        r_tekst += "<tb>" + table_name_adj[j] + "</tb>\n<content>" + text + "</content>\n"
        j += 1

    r_tekst += "</tables>\n"
    return r_tekst
            
   
def GET_VERB(soup):
    table = soup.find('table')
    table_body = table.find('tbody')

    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    data3 = data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    #print(data)
    
    removable = ["Budućnost","Prošlost","Past","Future"]
    replaceable = {"Prezent" : "Present" , "Futur I." : "Future I", "Futur II." : "Future II", "Perfekt" : "Past Perfect", "Pluskvamperfekt" : "Past Pluperfect", "Imperfekt" : "Imperfect", "Aorist": "Aorist", "Kondicional I." : "Conditional I", "Kondicional II." : "Conditional II", "Imperativ" : "Imperative"}

    tekst = "Verbal forms,ja,ti,on / ona / ono,mi,vi,oni / one / ona,,"
    tekst0 = "null,Masculine singular,Feminine singular,Neuter singular,Masculine plural,Feminine plural,Neuter plural"
    tekst3 = "null,Present verbal adverb,Past verbal adverb,Verbal noun,,Other verbal forms,"

    ##Other verbal forms
    tekst3 += data3[1].split(": ")[1] + ","
    tekst3 += data3[2].split(": ")[1] + ","
    tekst3 += data3[3].split(": ")[1]
    tekst3 = AccomodateStringForFileWriting(tekst3)

    ##Main data
    for row in data:
        
        for item in removable:
            if item in row:
                row.remove(item)

        for item in replaceable:
            if row[0] == item:
                row[0] = replaceable[item]

        
        if len(row) < 3:
            continue
        elif "radni" in row[0] or "trpni" in row[0] or "Active" in row[0] or "Passive" in row[0]:
            
            if "radni" in row [0] or "Active" in row[0]:
                tekst0 += ",,Active past participle,"
            else:
                tekst0 += ",,Passive past participle,"    
            
            c1 = row[1].replace(" m. / "," / ").replace(" f. / "," / ").split(" / ")
            c2 = row[2].replace(" m. / "," / ").replace(" f. / "," / ").split(" / ")

            if c1[2].endswith(" n"):
                c1[2] = c1[2][0:-2]
            if c2[2].endswith(" n"):
                c2[2] = c2[2][0:-2]
            
            tekst0 += c1[0] + "," + c1[1] + "," + c1[2] + ","
            tekst0 += c2[0] + "," + c2[1] + "," + c2[2]

     
        else:
            for c in row:
                c = AccomodateStringForFileWriting(c)
                c = c.replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","")
                
                if row[0] == "Future I":
                    c = c.replace(" ću "," ću/")
                    c = c.replace(" ćeš "," ćeš/")
                    c = c.replace(" će "," će/")
                    c = c.replace(" ćemo "," ćemo/")
                    c = c.replace(" ćete "," ćete/")
                    c = c.replace(" će "," će/")
                    c = c.replace("/"," / ")

                tekst += c + ","

            tekst += ","

    tekst0 = tekst0.replace(" m,",",").replace(" f,",",").replace(" n,",",")

    tekst2 = "<tables>\n"
    tekst2 += "<tb>Past participle</tb>\n"
    tekst2 += "<content>" + tekst0 + "</content>\n"
    tekst2 += "<tb>Conjugation</tb>\n"
    tekst2 += "<content>" + tekst[0:-2] + "</content>\n"
    tekst2 += "<tb>Other verbal forms</tb>\n"
    tekst2 += "<content>" + tekst3 + "</content>\n"
    tekst2 += "</tables>\n"

    return tekst2

def GET_NOUN(soup):
    table = soup.find('table')
    table_body = table.find('tbody')

    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    data.pop(0)
    data = list(map(list, zip(*data)))
    data.pop(0)

    tekst = "null,nominative,genitive,dative,accusative,vocative,locative,instrumental,"

    tekst += ",singular,"
    for item in data[0]:
        tekst += item + ","

    tekst += ",plural,"
    for item in data[1]:
        tekst += item + ","
    
    tekst = tekst[0:-1]
    tekst = "<tables>\n<tb>Declension of </tb>\n<content>" + tekst + "</content>\n</tables>\n"
    
    return tekst