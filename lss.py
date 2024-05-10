import datetime
import json
import sys
import requests
import random
from datetime import datetime

def getJSON(kategori,key=None):
    with open(".config.json") as cfg:
        veri = json.load(cfg)
        donus = veri[kategori] if key == None else veri[kategori][key]
        return donus

rkir = "\033[1;31m"
ryes = "\033[1;32m"
rmav = "\033[1;34m"
rbitir = "\033[0m"

asembol = getJSON("ozellestirme","ayrac_sembol")
auzunluk = getJSON("ozellestirme","ayrac_uzunluk")

yardim = rmav+ asembol*auzunluk + rbitir + f'''
{ryes}YARDIM SAYFASI{rbitir} 
    
    TEMEL KOMUTLAR:
    {rmav}lss{rbitir} {rkir}[URL]{rbitir}
    {rmav}lss{rbitir} {rkir}[URL]{rbitir} {rkir}[KAYNAK]{rbitir}
    
    TEMEL KULLANIMLAR:
    {rmav}lss{rbitir} www.google.com    : cfg.json dosyasından rastgele API seçer
    {rmav}lss{rbitir} www.google.com k1 : cfg.json dosyasındaki k1 API'sini seçer
    
    EK KOMUTLAR:
    {rmav}lss{rbitir} {rkir}-h{rbitir}  : yardım sayfasını başlatır                      (help)
    {rmav}lss{rbitir} {rkir}-v{rbitir}  : versiyon numarası sayfasını başlatır           (versiyon)
    {rmav}lss{rbitir} {rkir}-u{rbitir}  : güncelleme varsa otomatik olarak günceller     (update)
    {rmav}lss{rbitir} {rkir}-g{rbitir}  : kısaltılan linkleri tarih damgası ile gösterir (geçmiş)
    {rmav}lss{rbitir} {rkir}-gs{rbitir} : kayıtların tutulduğu geçmişi siler             (geçmiş-sil)
    {rmav}lss{rbitir} {rkir}-pe{rbitir} : programı otomatik olarak pathe ekler           (path-ekle)
    {rmav}lss{rbitir} {rkir}-ta{rbitir} : tüm API'leri listeler                          (tüm-apiler)
    {rmav}lss{rbitir} {rkir}-a{rbitir}  : API ve özelleştirmeler için ayarları başlatır  (ayarlar)
    
    https://github.com/\033[1;36mwhy20w18\033[0m
'''+rmav+ asembol*auzunluk + rbitir

#random api ismi secer ve onu cevirir
def randomAPI():
    kaynak_sayisi = list(getJSON("kaynakAPI"))
    return random.choice(kaynak_sayisi[1:])

#shellden girilen ikinci argumana gore json dosyasindan api sec
def istekYapAPI(url,apiSec=randomAPI()):
    temizURL = "https://"+url+"/"
    ##python3 lss.py www.google.com k1 HATA STRING CEVIR
    API = getJSON("kaynakAPI",apiSec)
    r = requests.get(str(API)+temizURL)

    sonuc = r.text if r.status_code == 200 else "hata kodu:"+str(r.status_code)
    gecmis_kayit(temizURL,sonuc)
    return sonuc

def gecmis_kayit(url,shortURL):
    with open('.gecmis.txt','a') as gecmis:
        gecmis.write(url+"--->"+shortURL+"--->"+str(datetime.now())+"\n")
def gecmis_oku():
    dosya = open('.gecmis.txt','r')
    gecmis = dosya.read()
    print(gecmis)
    dosya.close()

def tum_apiler():
    

def main():
    ekKomutlar = {
        "-h": lambda : print(yardim),
        "-v": lambda : print(rmav+'lss versiyon 1.0.0'+rbitir,"github.com/why20w18",sep='\n'),
        "-u": lambda : print('updt'),
        "-g": gecmis_oku,
        "-gs": lambda : print(2),
        "-pe": lambda : print(2),
        "-ta": lambda : print(list(getJSON("kaynakAPI"))),
        "-a": lambda : print(2)
    }
    if len(sys.argv) == 1:
        print(rkir,'hiç parametre girmediniz yardım için "-h"',rbitir,sep='')
    elif len(sys.argv) > 3:
        print(rkir,'fazladan parametre girdiniz yardım için "-h"',rbitir,sep='')

    else:
        if sys.argv[1] in ekKomutlar:
            ekKomutlar[sys.argv[1]]()
        else:
            url = sys.argv[1]
            if len(sys.argv) == 3:
               print(ryes,"BASARILI[+]\n",rbitir,
                     rmav,istekYapAPI(url,sys.argv[2])
                     ,rbitir,sep='')
            else:
                print(ryes, "BASARILI[+]\n", rbitir,
                      rmav,istekYapAPI(url)
                      , rbitir,sep='')


if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    main()
else:
    print("python versiyonunuz:",sys.version_info,"\b\nlss için minimum python versiyonu 3.3'dür")