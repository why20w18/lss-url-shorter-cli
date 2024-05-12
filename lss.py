import json
import os
import sys
import requests
import random
from datetime import datetime
import subprocess
import time

versiyon = "lss_executable-v1.1.7-alpha"
rkir = "\033[1;31m"
ryes = "\033[1;32m"
rmav = "\033[1;34m"
rbitir = "\033[0m"

def gizleyici():
    listdir = os.listdir()
    for s in listdir:
        if s in ["config.json", "gecmis.txt", "pe.sh"]:
            os.system("mv " + s + " ." + s)

def getJSON(kategori,key=None):
    with open(os.getcwd()+"/.config.json") as cfg:
        veri = json.load(cfg)
        try:
            donus = veri[kategori] if key == None else veri[kategori][key]
        except KeyError as hata:
            print(rkir+'GECERSIZ PARAMETRELER GIRDINIZ !',rbitir)
            print("HATA : ",hata)
            quit()
        return donus

def setJSON(kategori, key, yeniKey):
    with open(".config.json", "r+") as cfg:
        veri = json.load(cfg)
        veri[kategori][key] = yeniKey
        cfg.seek(0)
        json.dump(veri, cfg,indent=4)


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
    
    {rmav}lss{rbitir} {rkir}-plls{rbitir}    : GNU projesi pllr2 desteği entegrasyonu sayfası (pllr2-lls)
    
    {rmav}lss{rbitir} {rkir}-v{rbitir}       : versiyon numarası sayfasını başlatır           (versiyon)
    {rmav}lss{rbitir} {rkir}-uc{rbitir}      : güncelleme varmi kontrol eder                  (update-check)
    {rmav}lss{rbitir} {rkir}-uc kur{rbitir}  : güncellemeyi otomatik olarak indirip kurar     (update-check-kur)
    
    {rmav}lss{rbitir} {rkir}-g{rbitir}       : kısaltılan linkleri tarih damgası ile gösterir (geçmiş)
    {rmav}lss{rbitir} {rkir}-gs{rbitir}      : kayıtların tutulduğu geçmişi siler             (geçmiş-sil)
        
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
    
    {rmav}lss{rbitir} {rkir}-a{rbitir} ackapa       : otomatik güncelleştirmeleri açıp kapatır              (./lss -uc DEVREDIŞI KALIR) 
    {rmav}lss{rbitir} {rkir}-a{rbitir} cfg          : config dosyasını düzenlemeyi başlatır                 (nano yüklü olmalıdır)
    {rmav}lss{rbitir} {rkir}-a{rbitir} sembol       : config ayraç değişimi özelleştirmesi
    {rmav}lss{rbitir} {rkir}-a{rbitir} uzunluk      : config ayraç uzunluğu özelleştirmesi
        
        
    {rmav}lss{rbitir} {rkir}-a{rbitir} os           : işletim sistemi bilgilerini getirir 
    
    {rmav}lss{rbitir} {rkir}-a{rbitir} gecmis       : geçmiş dosyasını düzenlemeyi başlatır                 (nano yüklü olmalıdır)
    
    https://github.com/\033[1;36mwhy20w18\033[0m
'''+rmav+ asembol*auzunluk + rbitir

#random api ismi secer ve onu cevirir
def randomAPI():
    kaynak_sayisi = list(getJSON("kaynakAPI"))
    return random.choice(kaynak_sayisi[1:])

#shellden girilen ikinci argumana gore json dosyasindan api sec
def istekYapAPI(url,apiSec=randomAPI()):
    temizURL = "https://"+url+"/"

    try:
        API = getJSON("kaynakAPI",apiSec) #VALUE GETIRIR

        #genel API ekleme semasi
        if apiSec != "k2":
            r = requests.get(str(API)+temizURL)
            sonuc = r.text if r.status_code == 200 else "hata kodu:" + str(r.status_code)
            gecmis_kayit(temizURL, sonuc)
            return sonuc

        elif apiSec == "k2":

            data = {
                "uzunlink": temizURL,
            }

            r = requests.post(API, data=data)

            if r.status_code == 200:
                sonuc = r.json()
                kisaLink = sonuc["url"]["kisA_URL"]
                return str(kisaLink)
            else:
                print("hata kodu:", r.status_code)


    except requests.exceptions.ConnectionError:
        print(rmav,"\bINTERNET COK YAVAS - ISTEK ZAMAN ASIMINA UGRADI",rbitir)
        quit()


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
    cfg_guncelleme = str(getJSON("ozellestirme", "guncelleme_kontrol"))
    try:

        if cfg_guncelleme:
            r = requests.get('https://api.github.com/repos/why20w18/lss-url-shorter-cli/releases/latest')
            guncel_release = r.json()
            guncel_versiyon = guncel_release["name"]
            dizin_adi = guncel_release["name"]
            guncelDegil = True
        else:
            print(rkir,'GUNCELLEME AYARLARINI KAPATTINIZ TEKRAR ACMAK ICIN ./lss -a help',rbitir,sep='')
            quit()

        try:
            if sys.argv[2] == "kur" and cfg_guncelleme:
                user = subprocess.check_output("whoami", shell=True).decode().strip()
                os.chdir("/home/"+user)
                os.mkdir(str(dizin_adi))


                print(rkir,"INDIRME BASLADI"+rbitir+"\n",sep='')
                print(rkir+"INDIRME KONUMU: /home/"+user+"/"+dizin_adi,rbitir)
                topindirme = len(guncel_release["assets"])
                for s in range(0,topindirme):
                    print(ryes + str(s + 1) + "/" + topindirme + " BASLADI",rbitir + rmav + "<->why20w18/lss-url-shorter-cli/releases/latest", rbitir)
                    time.sleep(2)
                    os.system("clear")
                    if guncel_release["assets"][s]["name"] == "lls":
                        os.chdir(str(dizin_adi))
                        subprocess.run(["wget", guncel_release["assets"][s]["browser_download_url"]])
                        os.chdir("/home/" + user)
                        continue

                    subprocess.run(["wget", guncel_release["assets"][s]["browser_download_url"]])
                for s in os.listdir():
                    if s in ["gecmis.txt","pe.sh","config.json"]:
                        os.system("cp "+s+" "+dizin_adi+"/")
                        os.system("mv "+s+" ."+s)

                os.system("clear")
                print(rbitir,ryes+"\n\nwhy20w18","\bINDIRME TAMAMLANDI[+]\n", rbitir,sep='\n')

                os.chdir(str(dizin_adi))
                os.chmod("lss",0o755)
                os.rmdir("/home/" + user + "/" + versiyon)

                print(ryes+"YETKILENDIRME TAMAMLANDI [+]"+rbitir)

                print(ryes,"GUNCELLEME BASARIYLA TAMAMLANDI [+]",rbitir,sep='')
                print(rkir+"PATH EKLEME ISLEMI BASLADI"+rbitir)
                path_ekle(dizin_adi)
                print(ryes+"PATH EKLEME ISLEMI TAMAMLANDI [+]"+rbitir)


                os.system("clear")
                print(rmav + guncel_versiyon + " BASLATILIYOR !\n\n\n\n" + rbitir)
                os.system("./lss -v && ./lss -uc")

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

def path_ekle(dizin_adi):
    kabuk = subprocess.check_output("echo $SHELL",shell=True).decode().strip()[5:]
    user = subprocess.check_output("whoami",shell=True).decode().strip()

    kabuk = "~/." + kabuk + "rc"
    eklenecek_dizin = "/home/"+user+"/"+dizin_adi

    os.chmod("pe.sh",0o755)

    print(ryes,"\bPATH ICIN IZINLER VERILDI",rbitir)
    os.system("./pe.sh "+eklenecek_dizin+" "+kabuk)


    print(ryes,"\b"+user +"adlı kullanıcının kullandığı "+kabuk+" adlı dizine lss eklenmiştir", rbitir)
    os.system("mv pe.sh .pe.sh")
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
        "-ta": tum_apiler,
    }
    ayarKomutlar = {
        "help" : lambda : print(yardim_ayarlar),
        "os" : lambda  : print("os"),
        "cfg" : lambda : ayarlar_cfg_baslat(True),
        "gecmis" : lambda : ayarlar_cfg_baslat(False),
        "sembol" : lambda : ayarlar_ozellestirme(True),
        "uzunluk": lambda : ayarlar_ozellestirme(False),
        "ackapa": lambda : ackapa()
    }
    if len(sys.argv) == 1:
        print(rkir,'hiç parametre girmediniz yardım için "-h"',rbitir,sep='')

    elif len(sys.argv) == 3 and sys.argv[2] in ["-a","-uc"]:
        if sys.argv[1] == "-a" and sys.argv[2] in ayarKomutlar:
            ayarKomutlar[sys.argv[2]]()
        elif sys.argv[1] == "-uc" and sys.argv[2] == "kur":
            guncellemeVarMi()

    elif len(sys.argv) > 3:
        print(rkir,'fazladan parametre girdiniz yardım için "-h"',rbitir,sep='')

    else:
        if sys.argv[1] in ekKomutlar:
            ekKomutlar[sys.argv[1]]()
        else:
            url = sys.argv[1]
            try:
                if len(sys.argv) == 3:
                   print(rmav+ asembol*auzunluk + rbitir+"\n"+ryes,"BASARILI[+]\n",rbitir,
                         rmav,istekYapAPI(url,sys.argv[2])
                         ,rbitir+"\n"+rmav+ asembol*auzunluk + rbitir,sep='')

                else:
                    print(rmav+ asembol*auzunluk + rbitir+"\n"+ryes, "BASARILI[+]\n", rbitir,
                          rmav,istekYapAPI(url)
                          ,rbitir,"\n"+rmav+ asembol*auzunluk + rbitir,sep='')

            except (requests.exceptions.InvalidSchema,requests.exceptions.InvalidURL,) as hata:
                print(rmav,'HATA : ',rbitir,rkir,hata,rbitir,'\nyanlış yada eksik URL girdiniz',sep='')




if sys.version_info.major == 3 and sys.version_info.minor >= 3:

    gizleyici()
    main()
else:
    print("python versiyonunuz:",sys.version_info,""
                                                  "\b\nlss için minimum python versiyonu 3.3'dür\n"
                                                  "python kurmak istemiyorsanız lss_executable versiyonu indirebilirsiniz")