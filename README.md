# Analiza prenosnih računalnikov

V tej projektni nalogi bom analiziral vse prenosnike, naprodaj na spletni trgovini [BigBang](https://www.bigbang.si/izdelki/racunalnistvo/prenosni-racunalniki/).

Za vsak prenosnik sem zajel podatke o:
* ceni
* znamki
* kategoriji
* prodajalcu
* popustu

Moj namen pri pripravi te naloge je bil ugotoviti, kakšna je povprečna cena prenosnikov glede na znamko in glede na kategorjio (poslovni, za vsakdanjo uporabo, gaming...). Zanimalo me je tudi, kakšne so razlike v številu prenosnikov glede na znamko in ali sta cena in odstotek popusta kaj povezana. Primerjati sem si jih želel tudi glede na oceno uporabnikov, ampak zaradi zelo majhnega števila glasov to ni bilo mogoče.

## Priprava

V datoteki zajempodatkov.py sem podatke zajel s strani [BigBang](https://www.bigbang.si/izdelki/racunalnistvo/prenosni-racunalniki/), jih izluščil s pomočjo regularnih izrazov in jih uredil v csv datoteko bigbang.csv. Potem sem jih predstavil v datoteki analiza.ipynb.