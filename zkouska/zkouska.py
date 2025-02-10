from collections import Counter
from itertools import count

# Funkce pro Shannon-Fanovo kódování
def vytvoreni_stromu(znaky, prefix=""):
    """Rekurzivní funkce pro Shannon-Fanovo kódování."""
    if len(znaky) == 1:
        char, _ = znaky[0]
        return {char: prefix}  # Vrátíme přiřazený kód
    
    # Rozdělení seznamu na dvě skupiny s co nejrovnoměrnějším součtem frekvencí
    total_freq = sum(freq for _, freq in znaky)
    running_sum = 0
    split_index = 0
    
    for i, (_, freq) in enumerate(znaky):
        running_sum += freq
        if running_sum >= total_freq / 2:
            split_index = i + 1
            break

    left_part = znaky[:split_index]
    right_part = znaky[split_index:]

    # Rekurzivně přiřazujeme 0 a 1
    codes = {}
    codes.update(vytvoreni_stromu(left_part, prefix + "0"))
    codes.update(vytvoreni_stromu(right_part, prefix + "1"))
    
    return codes

def kodovani(strom, text):
    vysledek = ""
    for znak in text:
        vysledek += strom[znak]

    velikost_paddingu = len(vysledek) % 8
    vysledek += "0" * velikost_paddingu

    return vysledek

def dekodovani(strom, zakodovany_text, velikost_paddingu):
    zakodovany_text = zakodovany_text[:-velikost_paddingu]

    obraceny_strom = {}
    for klic, hodnota in strom.items():
        obraceny_strom[hodnota] = klic

    dekodovany_text = ""
    buffer = ""

    for bit in zakodovany_text:
        buffer += bit
        if buffer in obraceny_strom:
            dekodovany_text += obraceny_strom[buffer]
            buffer = ""

    return dekodovany_text

vstup = "ahoj jak se mas"

cetnosti = Counter(vstup)

symboly = sorted(cetnosti.items(), key=lambda x: (-x[1], x[0]))
    
print()
print("vstup")
print(vstup)

print()
print("symboly")
print(symboly)

print()
print("strom")
strom = vytvoreni_stromu(symboly)
print(strom)

print()
print("zakodovany text")
zakodovany_text = kodovani(strom, vstup)
print(zakodovany_text)

print()
print("dekodovany text")
dekodovany_text = dekodovani(strom, zakodovany_text, 7)
print(dekodovany_text)



