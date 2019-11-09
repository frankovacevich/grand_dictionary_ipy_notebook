#WORDLIST_PATH = "C:/Users/fran_/Documents/Subtlebit/GRAND DICTIONARIES/AndroidApp/app/src/dict_croatian/assets/wordlist.xml"
WORDLIST_PATH = "wordlist2.xml"

word_dict = {}
#word_dict_ = {}


class word:
    english = []
    name = ""
    typ = ""
    tables = []
    tables_str = []
    webpage = ""

        
    def __init__(self):
        self.english = []
        self.name = ""
        self.typ = ""
        self.tables = []
        self.tables_str = []
        self.webpage = ""

    def __str__(self):
        return self.name + " (" + self.typ + "): " + self.english[0]

    def get_english(self):
        r = ""
        for item in self.english:
            if r != "":
                r += " / " + item
            else:
                r += item
        return replace_quotes(r)


def replace_quotes(string):
    return string.replace("/QUOTE/","'").replace('/DOUBLEQUOTE/','"')


##
current_word = None
with open(WORDLIST_PATH,'r',encoding='utf-8') as f:

    for line in f:
        if line.startswith("<ID>"):
            current_word = word()
            current_word.ID = line[4:line.find("</ID>")]

        if line.startswith("<name>"):
            current_word.name = line[6:line.find("</name>")]
            
        if line.startswith("<type>"):
            current_word.typ = line[6:line.find("</type>")]

        if line.startswith("<webpage>"):
            current_word.webpage = line[9:line.find("</webpage>")].split(",,")[1]
            
        if line.startswith("<en>"):
            current_word.english.append( line[4:line.find("</en>")] )

        if line.startswith("<content>"):
            current_word.tables_str.append(line[9:line.find("</content>")])
            
            index0 = 9
            if "Verb" in current_word.typ and "Present" in line:
                index0 = line.find("Present") + 8
            current_word.tables.extend(line[index0:line.find("</content>")].replace(" / ",",").replace("/",",").replace(" - ",",").replace("-",",").replace(",,",",").split(","))
            
        if line.startswith("</word>"):
            #if current_word.name in word_dict:
            #    word_dict[current_word.name + "2"] = current_word 
            #else:
            #    word_dict[current_word.name] = current_word  

            if current_word.name not in word_dict:
                word_dict[current_word.name] = []
            word_dict[current_word.name].append(current_word)
                


    f.close()


inverse_dict = {}

for word in word_dict:
    for item in word_dict[word]:
        for subitem in item.tables:
            
            if item.typ == "Pronoun":
                if "instrumental" in item.english[0] or "vocative" in item.english[0] or "locative" in item.english[0] or "accusative" in item.english[0] or "genitive" in item.english[0] or "dative" in item.english[0]:
                    continue
            
            if subitem not in inverse_dict:
                inverse_dict[subitem] = []
            if word not in inverse_dict[subitem]:
                inverse_dict[subitem].append(word)
                
    if word not in inverse_dict:
        inverse_dict[word] = []
        inverse_dict[word].append(word)

    if word.endswith("ti"):
        if word[0:-1] not in inverse_dict:
            inverse_dict[word[0:-1]] = []
        inverse_dict[word[0:-1]].append(word)


aux_ = {}
for w in inverse_dict:
    if "(" in w and (w[-2] == "(" or w[-3] == "("):
        
        word_without_p = w[:w.find("(")]
        aux_[word_without_p] = inverse_dict[w]
        aux_[word_without_p + "a"] = inverse_dict[w]
        aux_[word_without_p + "e"] = inverse_dict[w]
        aux_[word_without_p + "u"] = inverse_dict[w]

    if "(" in w and ")" in w and w[-2] != "(" and w[-3] != "(":
        aux_[w.replace("(","").replace(")","")] = inverse_dict[w]
        aux_[w.replace(w[w.find("("):w.find(")")+1],"")] = inverse_dict[w]

    if len(w) > 1:
        if w[0] == w[0].upper():
            aux_[w[0].lower() + w[1:]] = inverse_dict[w]



aux_["nisam"] = ["biti"]
aux_["nisi"] = ["biti"]
aux_["nije"] = ["biti"]
aux_["nismo"] = ["biti"]
aux_["niste"] = ["biti"]
aux_["nisu"] = ["biti"]

aux_["neću"] = ["htjeti"]
aux_["nećeš"] = ["htjeti"]
aux_["neće"] = ["htjeti"]
aux_["nećemo"] = ["htjeti"]
aux_["nećete"] = ["htjeti"]

aux_["u"] = "u"
aux_["a"] = "a"
aux_["g."] = "godina"

for item in aux_:
    inverse_dict[item] = aux_[item]

to_remove = ['null', 'nominative', 'genitive', 'dative', 'accusative', 'vocative', 'locative', 'instrumental', 'singular', 'plural','common','neuter','e','','m','n','f']
for r in to_remove:
    if r in inverse_dict:
        inverse_dict.pop(r)

inverse_dict["kaj"] = ['gdo', 'kaj', '(k)teroga', 'česa', '(k)terem', 'čemu', '(k)terom(u)', 'čem', 'kteroga', 'teroga', 'kterem', 'terem']