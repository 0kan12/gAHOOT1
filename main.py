
from threading import Thread
from flask import request,render_template,jsonify,redirect
import random,string,flask,json,hashlib,os,qrcode,threading,time
soru_num=0
base_url="https://ray-humane-hagfish.ngrok-free.app"
locps="AAACB03965D253F1A1C779169EA7B689E0DC52F8BE8BEABDFB9C20946F2A4EB9"
from time import sleep
app=flask.Flask(__name__)
bos_sorular={"puan":"0","s1":"","s2":"","s3":"","s4":"","s5":"","s6":"","s7":"","s8":"","s9":"","s10":""}
def generate_room_code():
    code=""
    for i in range(6):
        code+=(random.choice(string.digits))
    return code
def check_name1(username1):
    for character in username1:
        if not (character in string.digits or character in string.ascii_lowercase or character in string.ascii_uppercase or character==" "):
            return False
    return True
def run():
    app.run(host='0.0.0.0', port=80)
def keep_alive():
    t = Thread(target=run)
    t.start()

def create_room():
    veri_klasoru = "veriler"  # Veriler klasörünün adı
    dosya_yolu = os.path.join(veri_klasoru, "odalar.json")
    try:
        with open(dosya_yolu, 'r') as dosya:
            odalar = json.load(dosya)
    except FileNotFoundError:
        if not os.path.exists(veri_klasoru):
            os.makedirs(veri_klasoru)
        odalar = {"odalar": []}
    oda = {
        "odano": generate_room_code(),
        "odadakiler": [],
        "soru_sayisi":"0",
        "room_status":"-",
        "kalan_sure":"0",
        "cevap_sayisi":"0",
        "mevcut_oyuncu":"0"
   }
    odalar["odalar"].append(oda)
    with open(dosya_yolu, 'w') as dosya:
        json.dump(odalar, dosya, indent=4)
    return oda['odano']
def create_qrcode(data,filename):
    url=f'{base_url}/?room_code={data}'
    img=qrcode.make(url)
    img.save(f"static/qrcodes/{filename}.png")
    return filename+".png"
def soru_cek(soru_no):
    veri_klasoru = "veriler" 
    dosya_yolu = os.path.join(veri_klasoru, "sorular.json")
    with open(dosya_yolu,"r",encoding="utf-8") as file:
        data=json.load(file)
    for indeks, soru in enumerate(data['sorular']):
        indeks+=1
        if indeks==soru_no:
            return [soru,indeks]
def kullanici_ekle(oda_no, yeni_kullanici):
    oda_indeksi=0
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == oda_no:
            oda_indeksi = indeks
            break
    if oda_indeksi is not None:
        print(yeni_kullanici)
        odalar["odalar"][oda_indeksi]["odadakiler"].append({yeni_kullanici:bos_sorular})
        with open(dosya_yolu, 'w') as dosya:
            json.dump(odalar, dosya, indent=4,ensure_ascii=True)
    else:
        print(f"{oda_no} numaralı oda bulunamadı.")
def check_name(room_code,name):
    oda_indeksi=0
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == room_code:
            oda_indeksi = indeks
            break
    if oda_indeksi is not None:
        for kisi in odalar["odalar"][oda_indeksi]["odadakiler"]:
            for a in kisi.keys():
                print(a)
                if a==name:
                    
                    return False
        return True
def check_room_is_valid(room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            return False
    return True

def get_soru_no(roomcode):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            return oda.get("soru_sayisi")
def change_soru_no(roomcode):
    oda_indeksi=0
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            oda_indeksi = indeks
            break
    if oda_indeksi is not None:
        odalar["odalar"][oda_indeksi]["soru_sayisi"]=str(int(odalar["odalar"][oda_indeksi]["soru_sayisi"])+1)
        with open(dosya_yolu, 'w') as dosya:
            json.dump(odalar, dosya, indent=4)
def change_mevcut_oyuncu(roomcode):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            oda_indeksi = indeks
            odalar["odalar"][oda_indeksi]["mevcut_oyuncu"]=str(int(odalar["odalar"][oda_indeksi]["mevcut_oyuncu"])+1)
            with open(dosya_yolu, 'w') as dosya:
                json.dump(odalar, dosya, indent=4)
def get_mevcut_oyuncu(roomcode):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            return oda.get("mevcut_oyuncu")
def change_cevap_sayisi(roomcode,value:bool):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            oda_indeksi = indeks
            if value==False:
                odalar["odalar"][oda_indeksi]["cevap_sayisi"]=str(0)
            else:
                odalar["odalar"][oda_indeksi]["cevap_sayisi"]=str(int(odalar["odalar"][oda_indeksi]["cevap_sayisi"])+1)
            with open(dosya_yolu, 'w') as dosya:
                json.dump(odalar, dosya, indent=4)
def get_cevap_sayisi(roomcode):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, 'r') as dosya:
        odalar = json.load(dosya)
    for indeks, oda in enumerate(odalar["odalar"]):
        if oda.get("odano") == roomcode:
            return oda.get("cevap_sayisi")
def get_valid_plrs(room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            persons=[]
            for person in oda.get("odadakiler"):
                aw=str(person.keys())
                aw1=aw.replace("dict_keys(['","")
                aw2=aw1.replace("'])","")
                persons.append(aw2)
            return persons

def change_room_status(room_code,değer:bool):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
    if oda_indeksi is not None:
        if değer==True:
            odalar["odalar"][oda_indeksi]["room_status"]="+"
        else:
            odalar["odalar"][oda_indeksi]["room_status"]="-"
        with open(dosya_yolu, 'w') as dosya:
            json.dump(odalar, dosya, indent=4)
def get_room_status(room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            return oda.get("room_status")
def ent_ans(room_code,username,cevap,soruno):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                    if key==username:
                        kisi_indeks=indeks
                        print(odalar["odalar"][oda_indeksi]["odadakiler"][kisi_indeks][username][soruno])
                        odalar["odalar"][oda_indeksi]["odadakiler"][kisi_indeks][username][soruno] = cevap
                        with open(dosya_yolu, "w") as dosya:
                            json.dump(odalar, dosya, indent=4)
def puan_ver(puan,username,room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                    if key==username:
                        kisi_indeks=indeks
                        odalar["odalar"][oda_indeksi]["odadakiler"][kisi_indeks][username]['puan']=str(int(odalar["odalar"][oda_indeksi]["odadakiler"][kisi_indeks][username]['puan'])+puan)
                        with open(dosya_yolu, "w") as dosya:
                            json.dump(odalar, dosya, indent=4)
def get_points(room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    puanlar=[]
    for indeks1, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks1
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                        puanlar.append([key,odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key]['puan']]) 
    if len(puanlar)<5:
            for i in range(5-(len(puanlar))):
                puanlar.append(["boş",0])
    siralanmis_liste =sorted( puanlar,reverse=True,key=lambda x: int(x[1]))
    return siralanmis_liste
def get_user_sira(room_code, username):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, "r") as dosya:
        odalar = json.load(dosya)
    puanlar = []
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano") == str(room_code):
            oda_indeksi = indeks
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                    puanlar.append([key, odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key]['puan']])
    if len(puanlar) < 5:
        for i in range(5 - len(puanlar)):
            puanlar.append(["boş", 0])
    siralanmis_liste = sorted(puanlar, reverse=True, key=lambda x: int(x[1]))
    kullanici_siralamasi = None
    for indeks, (kullanici, puan) in enumerate(siralanmis_liste, start=1):
        if kullanici == username:
            kullanici_siralamasi = indeks
            break

    return  kullanici_siralamasi
def get_kalan_sure(room_code):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
    if oda_indeksi is not None:
        return odalar["odalar"][oda_indeksi]["kalan_sure"]
def eksilt():
    while True:
        time.sleep(1)
        dosya_yolu = os.path.join("veriler", "odalar.json")
        with open(dosya_yolu,"r") as dosya:
            odalar=json.load(dosya)
            for indeks, oda in enumerate(odalar['odalar']):
                if int(odalar["odalar"][indeks]["kalan_sure"])>-1:
                    odalar["odalar"][indeks]["kalan_sure"]=str(int(odalar["odalar"][indeks]["kalan_sure"])-1)
                    with open(dosya_yolu, "w") as dosya:
                        json.dump(odalar, dosya, indent=4)
def change_kalan_sure(room_code,value):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
    if oda_indeksi is not None:
         odalar["odalar"][oda_indeksi]["kalan_sure"]=value
         with open(dosya_yolu, "w") as dosya:
            json.dump(odalar, dosya, indent=4)
def get_soru_cevaplari():
    dosya_yolu = os.path.join("veriler", "sorular.json")
    with open(dosya_yolu,"r") as dosya:
        data=json.load(dosya)
    cevaplar={}
    for a,soru in enumerate(data['sorular']):
        cevaplar[str(a+1)]=soru['dogru_cevap']
    return cevaplar
def get_dy_sayisi(room_code,username):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==room_code:
            for kisi_indeks,persons in enumerate(oda.get("odadakiler")):
                for name in persons.keys():
                    if name==username:
                        oyuncu_cevapları={'ds':0,'ys':0}
                        for no,soru in enumerate(odalar['odalar'][indeks]['odadakiler'][kisi_indeks][username]):
                            if no>0:
                                if odalar['odalar'][indeks]['odadakiler'][kisi_indeks][username][soru]==get_soru_cevaplari()[str(no)]:
                                    oyuncu_cevapları['ds']+=1
                                else:
                                    oyuncu_cevapları["ys"]+=1
                        return oyuncu_cevapları
def check_soru_of_no(soruno,room_code,username):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==room_code:
            for kisi_indeks,persons in enumerate(oda.get("odadakiler")):
                for name in persons.keys():
                    if name==username:
                        for no,soru in enumerate(odalar['odalar'][indeks]['odadakiler'][kisi_indeks][username]):
                            if str(no)==str(soruno):
                                if odalar['odalar'][indeks]['odadakiler'][kisi_indeks][username][soru]==get_soru_cevaplari()[str(no)]:
                                    return "+"
                                else:
                                    return "-"
def get_all_data(room_code):
    data={}
    for person in get_points(room_code):
        if person[0]!="boş" and person[0]!="0":
            data[person[0]]={
                "puan":get_puan(room_code,person[0]),
                "ds":get_dy_sayisi(room_code,person[0])['ds'],
                "ys":get_dy_sayisi(room_code,person[0])['ys'],
                "sorular":{'s1':check_soru_of_no(1,room_code,person[0]),"s2":check_soru_of_no(2,room_code,person[0]),"s3":check_soru_of_no(3,room_code,person[0]),"s4":check_soru_of_no(4,room_code,person[0]),"s5":check_soru_of_no(5,room_code,person[0]),"s6":check_soru_of_no(6,room_code,person[0]),"s7":check_soru_of_no(7,room_code,person[0]),"s8":check_soru_of_no(8,room_code,person[0]),"s9":check_soru_of_no(9,room_code,person[0]),"s10":check_soru_of_no(10,room_code,person[0])}
                }
    return data


def get_answer_amount(room_code,soru_no):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    cevaplar={"A":0,"B":0,"C":0,"D":0}
    for oda_indeksi, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                        if odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key][soru_no]=="A":
                            cevaplar["A"]+=1
                        elif odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key][soru_no]=="B":
                            cevaplar["B"]+=1
                        elif odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key][soru_no]=="C":
                            cevaplar["C"]+=1
                        elif odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key][soru_no]=="D":
                            cevaplar["D"]+=1
    return cevaplar
def check_answer(room_code,username):
    dosya_yolu = os.path.join("veriler","odalar.json")
    with open(dosya_yolu,"r") as dosya:
        odalar=json.load(dosya)
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano")==str(room_code):
            oda_indeksi=indeks
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                    if key==username:
                        soru=soru_cek(int(get_soru_no(room_code)))
                        if  odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key][f's{get_soru_no(room_code)}']==soru[0]['dogru_cevap']:
                            return True
    return False
def calc_puan(zaman1):
    zaman=int(zaman1)
    sikma=30-int(zaman)
    return 1000-sikma*30
def get_puan(room_code,username):
    dosya_yolu = os.path.join("veriler", "odalar.json")
    with open(dosya_yolu, "r") as dosya:
        odalar = json.load(dosya)
    puanlar = []
    for indeks, oda in enumerate(odalar['odalar']):
        if oda.get("odano") == str(room_code):
            oda_indeksi = indeks
            for indeks, oda1 in enumerate(oda.get("odadakiler")):
                for key in oda1.keys():
                    if key==username:
                        return odalar["odalar"][oda_indeksi]["odadakiler"][indeks][key]['puan']
@app.route("/")
def main():
    try:
        room_code=request.args.get("room_code")
    except:
        room_code=None
    return render_template("code.html",room_code=room_code,a="Katıl")
@app.route("/waitingroom")
def hoppala():
    auth=request.args.get("auth")
    token=request.args.get("token")
    room_code=request.args.get("room_code")
    if token==locps:
        return render_template("waitingroom.html",username=auth,room_code=room_code,puan=0)
    else:
        return "forbidden"
@app.route("/plr_reg",methods=['POST','GET'])
def plr_register():
    room_code=request.form['room_code']
    username=request.form['username']

    if username=="" or room_code=="":
        return render_template("code.html",a="username veya roomcode boş")
    if int(get_soru_no(room_code))!=0:
        return render_template("code.html",a="oyun çoktan başladı :(")
    if not check_name1(username):
        return render_template("code.html",a="girdiğiniz isim geçersiz karakterler içeriyor")
    if not check_name(room_code,username):
        return render_template("code.html",a="bu isim zaten var")
    
    if not check_room_is_valid(room_code):
        change_mevcut_oyuncu(room_code)
        kullanici_ekle(room_code,username)
        return redirect(f'{base_url}/waitingroom?auth={username}&token={locps}&room_code={room_code}')
    return render_template("code.html",a="oda mevcut değil")

@app.route("/son")
def fesdghf():
    room_code=request.args.get("room_code")
    return render_template("son.html",data=get_all_data(room_code))

@app.route("/fast_join")
def fast_join1():
    room_code=request.args.get("room_code")
    return redirect(f'{base_url}/?room_code={room_code}')
@app.route("/get_players")
def get_plrs():
    room_code=request.args.get('room_code')
    return get_valid_plrs(room_code)
@app.route("/new_question")
def check_rq():
    room_code=request.args.get('room_code')
    if get_soru_no(room_code)=="10":
        return redirect(f'{base_url}/son?room_code={room_code}')
    if get_soru_no(room_code)=="0":
        change_room_status(room_code,True)
    change_cevap_sayisi(room_code,False)
    change_kalan_sure(room_code,30)
    change_soru_no(room_code)
    soru=soru_cek(int(get_soru_no(room_code)))
    print(soru)
    return render_template("main.html",room_code=room_code,soru=soru[0]['soru'],secenek_a=soru[0]['secenek_a'],secenek_b=soru[0]['secenek_b'],secenek_c=soru[0]['secenek_c'],secenek_d=soru[0]['secenek_d'],soru_sayisi=(soru[1]))
@app.route("/leaderboard")
def get_leaderboard():
    puanlar=get_points(request.args.get("room_code"))
    return render_template("leaderboard.html",room_code=request.args.get("room_code"),a1=puanlar[0][0],puan1=puanlar[0][1],a2=puanlar[1][0],puan2=puanlar[1][1],a3=puanlar[2][0],puan3=puanlar[2][1],a4=puanlar[3][0],puan4=puanlar[3][1],a5=puanlar[4][0],puan5=puanlar[4][1])
@app.route("/notfound")
def error31():
    return render_template("error31.html")
@app.route("/hosting")
def asp12():
    room_code=request.args.get("room_code")
    password=request.args.get("password")
    if password==locps:
        return render_template("test.html",room_code=room_code,soru_no=get_soru_no(room_code),image_filename=create_qrcode(room_code,room_code))
    else:
        return redirect(f"{base_url}/notfound")
@app.route("/client_ctrlr")
def client1():
    room_code=request.args.get("room_code")
    username=request.args.get("username")
    return render_template("telgame.html",username=username,room_code=room_code,soruno=get_soru_no(room_code),puan=get_puan(room_code,username))
@app.route("/client_router")
def client():
    room_code=request.args.get("room_code")
    if get_room_status(room_code)=="+":
        return jsonify("true")
    return jsonify("false")
@app.route("/istatistikler")
def sdfgh():
    room_code=request.args.get("room_code")
    return render_template("grafik.html",room_code=room_code,a=get_answer_amount(room_code,f's{get_soru_no(room_code)}')["A"],b=get_answer_amount(room_code,f's{get_soru_no(room_code)}')["B"],c=get_answer_amount(room_code,f's{get_soru_no(room_code)}')["C"],d=get_answer_amount(room_code,f's{get_soru_no(room_code)}')["D"],soru_no=get_soru_no(room_code))
@app.route("/duryolcu")
def snd():
    room_code=request.args.get("room_code")
    username=request.args.get("username")
    cevap=request.args.get("answer")
    zaman=get_kalan_sure(room_code)
    print(zaman)
    change_cevap_sayisi(room_code,True)
    ent_ans(room_code,username,cevap,f's{get_soru_no(room_code)}')
    return render_template("bekle.html",username=username,puan=get_puan(room_code,username),room_code=room_code,answer=cevap,time=zaman)
@app.route("/check_cevap")
def sdfgwefghj():
    room_code=request.args.get("room_code")
    username=request.args.get("username")
    time=request.args.get("time")
    try:
        if check_answer(room_code,username):
            puan_ver(calc_puan(int(time)),username,room_code)
            return redirect(f'{base_url}/dogru?username={username}&room_code={room_code}&puan1={calc_puan(int(time))}')
        return redirect(f'{base_url}/yanlis?username={username}&room_code={room_code}')
    except:
        sleep(0.5)
        if check_answer(room_code,username):
            puan_ver(calc_puan(int(time)),username,room_code)
            return redirect(f'{base_url}/dogru?username={username}&room_code={room_code}&puan1={calc_puan(int(time))}')
        return redirect(f'{base_url}/yanlis?username={username}&room_code={room_code}')
@app.route("/get_kalan_sure")
def sdfghg():
    room_code=request.args.get("room_code")
    if int(get_kalan_sure(room_code))>-1 and get_cevap_sayisi(room_code)!=get_mevcut_oyuncu(room_code):
        return jsonify("true")
    return jsonify("false")
@app.route("/hostgame")
def check_host():
    password=request.args.get('id')
    if password==locps:
        return redirect(f'{base_url}/hosting?room_code={create_room()}&password={locps}')
    else:
        return redirect(f"{base_url}/notfound")
@app.route("/get_kalan_sure1")
def get_31():
    room_code=request.args.get("room_code")
    if get_cevap_sayisi(room_code)==get_mevcut_oyuncu(room_code):
        return "0"
    return get_kalan_sure(request.args.get("room_code"))
@app.route("/dogru")
def ghjk():
    username=request.args.get("username")
    room_code=request.args.get("room_code")
    puan1=request.args.get("puan1")
    return render_template("sonuc_dogru.html",puan31=puan1,username=username,sıra_no=get_user_sira(room_code,username),puan=get_puan(room_code,username),room_code=room_code)
@app.route("/yanlis")
def yanlis_cevap():
    username=request.args.get("username")
    room_code=request.args.get("room_code")
    return render_template("sonuc_yanlis.html",username=username,sıra_no=get_user_sira(room_code,username),puan=get_puan(room_code,username),room_code=room_code)

"""
okan baba pro tarafından hazırlandı hazırlanma sebebi bir taş ile 6 kuş vurmak 
:) kodu çaldıysan buraları silme pls
"""
if __name__=="__main__":
    threading.Thread(target=eksilt).start()
    keep_alive()
