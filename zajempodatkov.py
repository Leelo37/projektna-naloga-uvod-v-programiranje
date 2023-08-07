import csv
import os
import requests
import traceback

bigbang_frontpage_url = 'https://www.bigbang.si/izdelki/racunalnistvo/prenosni-racunalniki/'
bigbang_directory = 'podatki'
frontpage_filename = 'bigbang.html'
csv_filename = 'bigbang.csv'


def download_url_to_string(url):
    try:
        page_content = requests.get(url)
        if page_content.status_code == 200:
            return page_content.text
        else:
            print(f"Čudna koda: {page_content.status_code} za url: {url} <-- če je stran (okoli) 60 to samo pomeni, da smo prišli do konca oglasov za prenosnike")
            return None
    except Exception:
        print(f"Prišlo je do spodnje napake pri dostopu do URL-ja {url}:\n{traceback.format_exc()}")
        return None

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(base_url, directory, filename):
    os.makedirs(directory, exist_ok=True)
    all_content = ""
    page_num = 1
    while True:
        page_url = f"{base_url}?page={page_num}"
        html_strani = download_url_to_string(page_url)
        if html_strani is not None:
            all_content += html_strani
            page_num += 1
        else:
            break
    
    save_string_to_file(all_content, directory, filename)

save_frontpage('https://www.bigbang.si/izdelki/racunalnistvo/prenosni-racunalniki/', bigbang_directory, frontpage_filename)

def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


import re

def page_to_ads(page_content):
    vzorec = r'<article class="clear cp".+?</article>'
    return re.findall(vzorec, page_content, flags=re.DOTALL)

#print(os.listdir())
vsebina = read_file_to_string(bigbang_directory, frontpage_filename)
oglasi = page_to_ads(vsebina)
#print(len(oglasi))

def get_dict_from_ad_block(block):
    vzorec_ime = r'<span style="display: none;" data-product_title=".+">(.+)</span>'
    vzorec_cena = r'<span style="display: none;" data-product_price=".+">(.+)</span>'
    vzorec_firma = r'<span style="display: none;" data-product_manufacturer_title=".+">(.+)</span>'
    vzorec_prodajalec = r'<span>Prodajalec: <a href="https://www.bigbang.si/prodajalec/.+">(.+)</a></span>'
    vzorec_kategorija = r'<span style="display: none;" data-product_category_title=".+">.+ > (.+)</span>'
    vzorec_popust = r'<div class="cp-badges">\n<div class="cp-badge cp-badge-discount">\n<span>-(.+)</span>\n<div class="cp-badge-tooltip cp-badge-tooltip-discount">Prihranek <strong>(.+)</strong></div>'
    try:
        ime = re.search(vzorec_ime, block).group(1)
        cena = re.search(vzorec_cena, block).group(1)
        firma = re.search(vzorec_firma, block).group(1)
        kategorija = re.search(vzorec_kategorija, block).group(1)
        prodajalec = re.search(vzorec_prodajalec, block).group(1)
        popust_procenti = re.search(vzorec_popust, block).group(1)
        popust_euro = re.search(vzorec_popust, block).group(2)

        slovar = {"ime": ime, "cena": cena, "firma": firma, "kategorija": kategorija, "prodajalec": prodajalec, "popust_procenti": popust_procenti, "popust_euro": popust_euro}
    except AttributeError:
        slovar = {"ime": ime, "cena": cena, "firma": firma, "kategorija": kategorija, "prodajalec": prodajalec, "popust_procenti": '0 %', "popust_euro": '0 €'}
    return slovar

#for oglas in oglasi:
#    print(get_dict_from_ad_block(oglas))

def ads_from_file(filename, directory):
    vsebina = read_file_to_string(directory, filename)
    oglasi = page_to_ads(vsebina)
    slovarji = []
    for oglas in oglasi:
        slovarji.append(get_dict_from_ad_block(oglas))
    return slovarji

#print(ads_from_file(frontpage_filename, bigbang_directory))

def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def write_bigbang_ads_to_csv(ads, directory, filename):
    assert ads and (all(slovar.keys() == ads[0].keys() for slovar in ads))
    imena_stolpcev = ads[0]
    write_csv(imena_stolpcev, ads, directory, filename)

vsi_slovarji = ads_from_file(frontpage_filename, bigbang_directory)
write_bigbang_ads_to_csv(vsi_slovarji, "podatki", csv_filename)

def main(redownload=True, reparse=True):
    pot_html = os.path.join(bigbang_directory, frontpage_filename)
    if redownload or not os.path.exists(pot_html):
        save_frontpage(bigbang_frontpage_url, bigbang_directory, frontpage_filename)
    else:
        print(f"Datoteka {pot_html} že obstaja")
    csv_mapa = "podatki"
    pot_csv = os.path.join(csv_mapa, csv_filename)
    if reparse or not os.path.exists(pot_csv):
        vsi_slovarji = ads_from_file(frontpage_filename, bigbang_directory)
        write_bigbang_ads_to_csv(vsi_slovarji, "podatki", csv_filename)
    else:
        print(f"Datoteka {pot_csv} že obstaja")

#main(False, False)