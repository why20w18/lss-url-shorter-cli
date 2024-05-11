import datetime
import json
import os
import sys
import requests
import random
from datetime import datetime
import subprocess


def getJSON(kategori,key=None):
    with open(os.getcwd()+"/.config.json") as cfg:
        veri = json.load(cfg)
        try:
            donus = veri[kategori] if key == None else veri[kategori][key]
        except KeyError as hata:
            print(rkir+'GECERSIZ PARAMETRELER GIRDINIZ !',rbitir)
            print("HATA : ",hata)
            #quit()
        return donus

def setJSON(kategori, key, yeniKey):
    with open(".config.json", "r+") as cfg:
        veri = json.load(cfg)
        veri[kategori][key] = yeniKey
        cfg.seek(0)
        json.dump(veri, cfg,indent=4)

versiyon = "lss_executable-v1.1.0-alpha"

rkir = "\033[1;31m"
ryes = "\033[1;32m"
rmav = "\033[1;34m"
rbitir = "\033[0m"

asembol = getJSON("ozellestirme","ayrac_sembol")
auzunluk = getJSON("ozellestirme","ayrac_uzunluk")

yardim = rmav+ asembol*auzunluk + rbitir + f'''
{ryes}YARDIM SAYFASI{rbitir} 
    
     MEVCUT VERSIYON: {rmav}{versiyon}{rbitir}
    
      TEMEL KOMUTLAR:
    {rmav}lss{rbitir} {rkir}[URL]{rbitir}
    {rmav}lss{rbitir} {rkir}[URL]{rbitir} {rkir}[KAYNAK]{rbitir}
    
      TEMEL KULLANIMLAR:
    {rmav}lss{rbitir} www.google.com         : cfg.json dosyasından rastgele API seçer
    {rmav}lss{rbitir} www.google.com k1      : cfg.json dosyasındaki k1 API'sini seçer
    
      EK KOMUTLAR:
    {rmav}lss{rbitir} {rkir}-h{rbitir}       : yardım sayfasını başlatır                      (help)
    
    {rmav}lss{rbitir} {rkir}-v{rbitir}       : versiyon numarası sayfasını başlatır           (versiyon)
    {rmav}lss{rbitir} {rkir}-uc{rbitir}      : güncelleme varmi kontrol eder                  (update-check)
    {rmav}lss{rbitir} {rkir}-uc kur{rbitir}  : güncellemeyi otomatik olarak indirip kurar     (update-check-kur)
    
    {rmav}lss{rbitir} {rkir}-g{rbitir}       : kısaltılan linkleri tarih damgası ile gösterir (geçmiş)
    {rmav}lss{rbitir} {rkir}-gs{rbitir}      : kayıtların tutulduğu geçmişi siler             (geçmiş-sil)
    
    {rmav}lss{rbitir} {rkir}-pe{rbitir}      : programı otomatik olarak pathe ekler           (path-ekle)
    
    {rmav}lss{rbitir} {rkir}-ta{rbitir}      : tüm API'leri listeler                          (tüm-apiler)
    
    {rmav}lss{rbitir} {rkir}-a help{rbitir}  : ayarlar komutunun yardım sayfasını başlatır    (ayarlar-help)
    
    https://github.com/\033[1;36mwhy20w18\033[0m
'''+rmav+ asembol*auzunluk + rbitir

yardim_ayarlar = rmav+ asembol*auzunluk + rbitir + f'''
{ryes}AYARLAR YARDIM SAYFASI{rbitir} 
    
     MEVCUT VERSIYON: {rmav}{versiyon}{rbitir}
    
      TEMEL KULLANIM:
    {rmav}lss{rbitir} {rkir}-a{rbitir} {rmav}IKINCIL_ARGUMAN{rbitir} 
    
      IKINCIL ARGUMANLAR:
    {rmav}lss{rbitir} {rkir}-a{rbitir} help         : ayarlar yardım sayfasını başlatır
    
    {rmav}lss{rbitir} {rkir}-a{rbitir} ackapa       : otomatik güncelleştirmeleri açıp kapatır (./lss -uc DEVREDIŞI KALIR) 
    {rmav}lss{rbitir} {rkir}-a{rbitir} config       : config dosyasını düzenlemeyi başlatır    (nano yüklü olmalıdır)
    {rmav}lss{rbitir} {rkir}-a{rbitir} sembol       : config ayraç değişimi özelleştirmesi
    {rmav}lss{rbitir} {rkir}-a{rbitir} uzunluk      : config ayraç uzunluğu özelleştirmesi
        
        
    {rmav}lss{rbitir} {rkir}-a{rbitir} os           : işletim sistemi bilgilerini getirir 
    
    {rmav}lss{rbitir} {rkir}-a{rbitir} gecmis       : geçmiş dosyasını düzenlemeyi başlatır    (nano yüklü olmalıdır)
    
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
    try:
        API = getJSON("kaynakAPI",apiSec)
        r = requests.get(str(API)+temizURL)
    except requests.exceptions.ConnectionError:
        print(rmav,"\bINTERNET COK YAVAS - ISTEK ZAMAN ASIMINA UGRADI",rbitir)
        quit()

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

def gecmis_sil():
    dosya = open('.gecmis.txt','w')
    print('SON SILINME TARIHI:',str(datetime.now()),file=dosya)
    dosya.close()
    print(ryes+"GECMIS KAYITLARI SILINDI[+]"+rbitir)
def tum_apiler():
    print(rmav,"KULLANILAN TUM APILER",rbitir,sep='')
    tum = getJSON("kaynakAPI")
    for s in dict(tum).values():
        if s == getJSON("kaynakAPI","kaynak_sayisi"):
            continue
        else:
            print(s)

def iversiyon():
    print("lss versiyon : ",rmav,versiyon,rbitir,sep='')

def guncellemeVarMi():
    #-uc argumani
    cfg_guncelleme = bool(getJSON("ozellestirme", "guncelleme_kontrol"))
    try:

        if cfg_guncelleme:
            r = requests.get('https://api.github.com/repos/why20w18/lss-url-shorter-cli/releases/latest')
            guncel_release = r.json()
            guncel_versiyon = guncel_release["name"]
            indirme_link = guncel_release["assets"][0]["browser_download_url"]
            boyut = round(int(guncel_release["assets"][0]["size"]) / (2**20),2) #mb
            guncelDegil = True
        else:
            print(rkir,'GUNCELLEME AYARLARINI KAPATTINIZ TEKRAR ACMAK ICIN ./lss -a help',rbitir,sep='')
            quit()

        try:
            if sys.argv[2] == "kur" and cfg_guncelleme:
                klasor = os.listdir(".")
                print('gerekli dosyalar kontrol ediliyor ...')
                if ".gecmis.txt" in klasor:
                    print('gerekli dosyalar kontrol edildi eksik yok')
                else:
                    os.system("touch .gecmis.txt")
                    print('eksik dosyalar olusturuldu')

                print("lss executable indirmesi başladı ...")
                os.system("mv lss lss_eski")

                print(rkir,"toplam indirme boyutu : ",boyut, "MB", rbitir+"\n",sep='')
                subprocess.run(["wget", indirme_link])

                print(rbitir,ryes+"\n\nwhy20w18","\bindirme tamamlandi", rbitir,sep='\n')
                os.chmod("lss",0o755)

                print(rmav,guncel_versiyon, "başlatılıyor !\n\n\n\n\nGIRILEN KOMUT:./lss -h\n",rbitir)
                os.system("./lss -h")

                print(rkir,"\n\n\nGUNCEL VERSIYONU KULLANMAK ICIN './lss -h' YAZIN",rbitir,sep='')
                guncelDegil = False

        except IndexError as hata:
            pass

        finally:
            if cfg_guncelleme and guncelDegil and versiyon != str(guncel_versiyon).strip():(
                print(ryes,"GUNCELLEME VAR !",rbitir
                      +"\n"+"yeni versiyon: ",
                      rmav,str(guncel_versiyon).strip()[:]
                      ,rbitir,sep=''))

            else:
                print(ryes+"lls EN GUNCEL VERSIYONDA !",rbitir+
                  "MEVCUT VERSIYON :" + guncel_versiyon,sep='\n')
    except requests.exceptions.ConnectionError:
        print(rmav,"\bINTERNET COK YAVAS - ISTEK ZAMAN ASIMINA UGRADI",rbitir)

def path_ekle():
    kabuk = subprocess.check_output("echo $SHELL",shell=True).decode().strip()[5:]
    user = subprocess.check_output("whoami",shell=True).decode().strip()

    kabuk = "~/." + kabuk + "rc"
    eklenecek_dizin = os.getcwd()
    os.chmod("lss.sh",0o755)
    os.chmod(".pe.sh",0o755)

    print(ryes,"\bPATH ICIN IZINLER VERILDI",rbitir)
    os.system("./.pe.sh "+eklenecek_dizin+" "+kabuk)

    print(ryes,"\b"+user +"adlı kullanıcının kullandığı "+kabuk+" adlı dizine lss eklenmiştir", rbitir)

def ackapa():
    durum = str(getJSON("ozellestirme","guncelleme_kontrol"))
    oto_guncel_acikMi =  durum.isspace()
    print(ryes,"\bILK DURUM : OTOMATIK GUNCELLEME ACIK : ",oto_guncel_acikMi,rbitir)
    if oto_guncel_acikMi:
        setJSON("ozellestirme","guncelleme_kontrol","")
        print(rkir,"\bSON DURUM : OTOMATIK GUNCELLEME KAPATILDI './lss -uc' DEVREDISI KALDI !",rbitir)

    else:
        setJSON("ozellestirme", "guncelleme_kontrol", " ")
        print("SON DURUM : OTOMATIK GUNCELLEME ACILDI")

def ayarlar_cfg_baslat(cfgMi):
    ls = os.listdir()
    for s in ls:
        if cfgMi:
            subprocess.run(["nano",".config.json"])
            break
        else:
            subprocess.run(["nano", ".gecmis.txt"])
            break
    else:
        print(rkir,'\bdizinde aranan dosya bulunmuyor !',rbitir)

def ayarlar_ozellestirme(ayracMi):
    if ayracMi:
        ayracSembol = getJSON("ozellestirme","ayrac_sembol")
        istek_sembol = input("eski sembol:"+ayracSembol+"\n\byeni sembolü giriniz >")
        setJSON("ozellestirme","ayrac_sembol",istek_sembol)
        print(ryes,"\bAYRAC DEGISTIRILMISTIR !",rbitir)
    else:
        uzunluk = getJSON("ozellestirme", "ayrac_uzunluk")
        yeniUzunluk = int(input("eski uzunluk:"+str(uzunluk)+"\n\byeni uzunluk giriniz >"))
        setJSON("ozellestirme", "ayrac_uzunluk", yeniUzunluk)
        print(ryes, "\bAYRAC UZUNLUGU DEGISTIRILMISTIR !", rbitir)

def main():
    ekKomutlar = {
        "-h": lambda : print(yardim),
        "-v": iversiyon,
        "-uc": lambda : guncellemeVarMi(),
        "-g": gecmis_oku,
        "-gs": gecmis_sil,
        "-pe": lambda : path_ekle(),
        "-ta": tum_apiler,
        "-a": lambda : print("ayarlar yardım sayfası için '-a help' girin")
    }
    ayarKomutlar = {
        "help" : lambda : print(yardim_ayarlar),
        "os" : lambda  : print("os"),
        "config" : lambda : ayarlar_cfg_baslat(True),
        "gecmis" : lambda : ayarlar_cfg_baslat(False),
        "sembol" : lambda : ayarlar_ozellestirme(True),
        "uzunluk": lambda : ayarlar_ozellestirme(False),
        "ackapa": lambda : ackapa()
    }
    if len(sys.argv) == 1:
        print(rkir,'hiç parametre girmediniz yardım için "-h"',rbitir,sep='')
    elif len(sys.argv) > 3:
        print(rkir,'fazladan parametre girdiniz yardım için "-h"',rbitir,sep='')
    elif len(sys.argv) == 3:
        if sys.argv[1] in "-a" and sys.argv[2] in ayarKomutlar:
            ayarKomutlar[sys.argv[2]]()
    else:
        if sys.argv[1] in ekKomutlar:
            ekKomutlar[sys.argv[1]]()
        else:
            url = sys.argv[1]
            try:
                if len(sys.argv) == 3:
                   print(rmav+ asembol*auzunluk + rbitir+"\n"+ryes,"BASARILI[+]\n",rbitir,
                         rmav,istekYapAPI(url,sys.argv[2])
                         ,rbitir+rmav+ asembol*auzunluk + rbitir,sep='')
                else:
                    print(rmav+ asembol*auzunluk + rbitir+"\n"+ryes, "BASARILI[+]\n", rbitir,
                          rmav,istekYapAPI(url)
                          , rbitir,rmav+ asembol*auzunluk + rbitir,sep='')
            except (requests.exceptions.InvalidSchema,requests.exceptions.InvalidURL,) as hata:
                print(rmav,'HATA : ',rbitir,rkir,hata,rbitir,'\nyanlış yada eksik URL girdiniz',sep='')

if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    main()
else:
    print("python versiyonunuz:",sys.version_info,""
                                                  "\b\nlss için minimum python versiyonu 3.3'dür\n"
                                                  "python kurmak istemiyorsanız lss_executable versiyonu indirebilirsiniz")