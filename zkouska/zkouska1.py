from collections import Counter #pouzivam ke spocitani cetnosti
import ast # pouzivam k prevodu strom stringu na strom slovnik

def vytvoreni_stromu(znaky, prefix=""):
    
    # podminka k zastabeni rekurze
    if len(znaky) == 1: # zastaveni rekurze kdyz uz zbyva jenom jeden prvek
        znak, frekvence = znaky[0] # char dostane hodnotu prvniho prvku z dvojice 
        return {znak: prefix}  # vrati se slovnik, ve kterem je znak a jeho kod
    
    # rozdeleni seznamu na dve skupiny s co nejrovnomersim poctem vyskytu
    celkovy_soucet_frekvenci = sum(frekvence for znak, frekvence in znaky)
    postupny_soucet = 0
    index_rozdeleni = 0 # kde dojde k tomu, ze postupny soucet prekroci polovinu celkoveho souctu
    
    # tady hledam index rozdeleni
    # kdyz postupny soucet pretece polovinu celkoveho souctu, tak se cyklus zastavi a mame index
    for i, (znak, frekvence) in enumerate(znaky): # enumerate vrati tuple obsahujici index a hodnotu
        postupny_soucet += frekvence
        if postupny_soucet >= celkovy_soucet_frekvenci / 2:
            index_rozdeleni = i + 1 # seznam chceme rozdelit az po tomto prvku
            break

    # seznam se rozdeli na dve strany
    leva_strana = znaky[:index_rozdeleni] # od zacatku do indexu
    prava_strana = znaky[index_rozdeleni:] # od indexu do konce

    strom = {} # vyslkem je slovnik kde klice jsou znaky a hodnoty jsou kody jednotlivych znaku
    strom.update(vytvoreni_stromu(leva_strana, prefix + "0")) # rekurzivni volani pro levou stranu a priradime k prefixu 0
    strom.update(vytvoreni_stromu(prava_strana, prefix + "1")) # rekurzivni volani pro pravou stranu a priradime k prefixu 1
    
    return strom

def kodovani(strom, text):
    vysledek = ""

    # pro kazdy znak v textu, k vysledku se pripise hondnota znaku ze stromu 
    for znak in text:
        vysledek += strom[znak]

    # padding, kdyz neni delka vysledeku delitelna 8
    velikost_paddingu = len(vysledek) % 8
    vysledek += "0" * velikost_paddingu

    return vysledek

def dekodovani(strom, zakodovany_text, velikost_paddingu):
    zakodovany_text = zakodovany_text[:-velikost_paddingu] # odstraneni paddingu, druhy index je od konce napr -7

    obraceny_strom = {}
    # pro kazdy par klic hodnota ve stromu pridame do obraceneho stromu obraceny prvek
    for klic, hodnota in strom.items():
        obraceny_strom[hodnota] = klic

    dekodovany_text = ""
    binarni_kod = ""


    for bit in zakodovany_text:
        binarni_kod += bit
        if binarni_kod in obraceny_strom: # kdyz je binarni_kod v obracenem stromu
            dekodovany_text += obraceny_strom[binarni_kod] # do dekodovaneho textu se pripise hodnota podle klice v obracenem stromu
            binarni_kod = "" # resetuje se binarni kod

    return dekodovany_text



vyber1 = input("Chces provadet kodovani (k) nebo dekodovani (d)?: ")

if vyber1 == "k":
    vyber2 = input("Chces zadat text (t) nebo vlozit soubor (v)?: ")
    if vyber2 == "t":
        vstupni_text = input("Zadej text:\n")

        cetnosti = Counter(vstupni_text)

        symboly = sorted(cetnosti.items(), key=lambda x: (-x[1], x[0]))

        strom = vytvoreni_stromu(symboly)

        zakodovany_text = kodovani(strom, vstupni_text)

        with open("zakodovany_text.txt", "w") as file:
            file.write(str(strom)+"\n"+zakodovany_text)

        print()
        print("strom")
        print(strom)
        print()
        print("zakodovany text")
        print(zakodovany_text)

    elif vyber2 == "v":
        cesta_k_souboru = input("Zadej cestu k souboru:\n")

        with open(cesta_k_souboru, "r") as file:
            vstupni_text = file.read()

        cetnosti = Counter(vstupni_text)

        symboly = sorted(cetnosti.items(), key=lambda x: (-x[1], x[0]))

        strom = vytvoreni_stromu(symboly)

        zakodovany_text = kodovani(strom, vstupni_text)

        with open("zakodovany_text.txt", "w") as file:
            file.write(str(strom)+"\n"+zakodovany_text)

        print()
        print("strom")
        print(strom)
        print()
        print("zakodovany text")
        print(zakodovany_text)

    else:
        print("spatne zadany vyber")

elif vyber1 == "d":
    velikost_paddingu = int(input("Zadej velikost paddingu: "))
    cesta_k_souboru = input("Zadej cestu k souboru:\n")
    with open(cesta_k_souboru, "r") as file:
            strom_string = file.readline()
            vstupni_kod = file.readline()
    
    #print(strom_string)
    #print(vstupni_kod)

    strom_slovnik = ast.literal_eval(strom_string)

    #print(strom_slovnik)

    dekodovany_text = dekodovani(strom_slovnik, vstupni_kod, velikost_paddingu)

    with open("dekodovany_text.txt", "w") as file:
        file.write(dekodovany_text)

    print(dekodovany_text)

