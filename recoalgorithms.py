import pandas as pd

# Kullanıcı bilgilerini alma ve saklama
def kullanici_bilgileri_al():
    return {
        "yas": int(input("Yaşınızı girin: ")),
        "cinsiyet": input("Cinsiyetinizi girin (Erkek/Kadın): ").lower(),
        "kilo": float(input("Kilonuzu girin (kg): ")),
        "boy": float(input("Boyunuzu girin (cm): ")),
        "aktivite_durumu": input("Aktivite durumunuzu girin (hareketsiz/hafif/orta/çok/ekstra): ").lower()
    }

def bmh_hesapla(bilgiler):
    if bilgiler["cinsiyet"] == "erkek":
        return 10 * bilgiler["kilo"] + 6.25 * bilgiler["boy"] - 5 * bilgiler["yas"] + 5
    else:
        return 10 * bilgiler["kilo"] + 6.25 * bilgiler["boy"] - 5 * bilgiler["yas"] - 161

def tdee_hesapla(bmh, aktivite):
    aktivite_katsayilari = {
        "hareketsiz": 1.2,
        "hafif": 1.375,
        "orta": 1.55,
        "çok": 1.725,
        "ekstra": 1.9
    }
    return bmh * aktivite_katsayilari[aktivite]

def makro_ihtiyac_hesapla(tdee, cinsiyet, kilo, yas):
    karbonhidrat_ihtiyaci = (tdee * 0.55) / 4
    protein_ihtiyaci = kilo * 1.3  # Örnek olarak orta aktif seçeneği
    yag_ihtiyaci = (tdee * 0.25) / 9

    if cinsiyet == "erkek":
        lif_ihtiyaci = max(30, 38 - (yas % 10))
    else:
        lif_ihtiyaci = max(21, 25 - (yas % 10))

    return {
        "kalori": tdee,
        "karbonhidrat": karbonhidrat_ihtiyaci,
        "protein": protein_ihtiyaci,
        "yag": yag_ihtiyaci,
        "lif": lif_ihtiyaci
    }

def yemek_tuketimi_sorgula(dataset, yemek_adi, porsiyon):
    yemek_bilgileri = dataset[dataset["title"].str.lower() == yemek_adi]
    if yemek_bilgileri.empty:
        print("Girilen yemek bulunamadı. Lütfen datasetinizi kontrol edin.")
        return None
    else:
        yemek_bilgileri = yemek_bilgileri.iloc[0]
        return {
            "karbonhidrat": yemek_bilgileri["karbonhidrat"] * porsiyon,
            "protein": yemek_bilgileri["protein"] * porsiyon,
            "yag": yemek_bilgileri["yağ"] * porsiyon,
            "lif": yemek_bilgileri["lif"] * porsiyon,
            "kalori": yemek_bilgileri["kalori"] * porsiyon
        }

def kalan_ihtiyac_hesapla(ihtiyaclar, tuketim):
    return {
        "karbonhidrat": ihtiyaclar["karbonhidrat"] - tuketim["karbonhidrat"],
        "protein": ihtiyaclar["protein"] - tuketim["protein"],
        "yag": ihtiyaclar["yag"] - tuketim["yag"],
        "lif": ihtiyaclar["lif"] - tuketim["lif"],
        "kalori": ihtiyaclar["kalori"] - tuketim["kalori"]
    }

def filtreleme_ve_oneri(dataset, saat, kalan_ihtiyaclar):
    if 4 <= saat < 12:
        kategori = "kahvaltı"
    elif 12 <= saat < 15:
        kategori = "öğle yemeği"
    elif 15 <= saat < 17:
        kategori = "atıştırmalık"
    elif 17 <= saat < 22:
        kategori = "akşam yemeği"
    else:
        kategori = "atıştırmalık"

    filtrelenmis_yemekler = dataset[dataset["kategori"] == kategori]
    kalori_aralik = (kalan_ihtiyaclar["kalori"] * 0.85, kalan_ihtiyaclar["kalori"] * 1.15)
    onerilen_yemekler = filtrelenmis_yemekler[(filtrelenmis_yemekler["kalori"] >= kalori_aralik[0]) & (filtrelenmis_yemekler["kalori"] <= kalori_aralik[1])]

    return onerilen_yemekler

# Ana akış
kullanici_bilgileri = kullanici_bilgileri_al()

bmh = bmh_hesapla(kullanici_bilgileri)
tdee = tdee_hesapla(bmh, kullanici_bilgileri["aktivite_durumu"])
ihtiyaclar = makro_ihtiyac_hesapla(tdee, kullanici_bilgileri["cinsiyet"], kullanici_bilgileri["kilo"], kullanici_bilgileri["yas"])

print("\nGünlük İhtiyaçlarınız:")
for makro, miktar in ihtiyaclar.items():
    print(f"{makro.capitalize()}: {miktar:.2f}")

# Dataset yükleme (örnek olarak bir Excel dosyasından okunacak)
dataset = pd.read_excel("ornek_dosya.xlsx")

# Yemek önerisi al butonunu simüle etme
while True:
    print("\nYeni bir yemek önerisi için bilgileri girin.")
    secim = input("Seçiminizi yapın (yemek önerisi al/henüz yemek yemedim): ").lower()

    if secim == "henüz yemek yemedim":
        print("Henüz yemek yemediniz, ihtiyaçlarınız güncel olarak devam ediyor.")
    elif secim == "yemek önerisi al":
        saat = int(input("Şu anki saati girin (0-24): "))
        porsiyon = float(input("Yediğiniz porsiyon miktarını girin: "))
        yemek_adi = input("Yediğiniz yemeğin adını girin: ").lower()

        tuketim = yemek_tuketimi_sorgula(dataset, yemek_adi, porsiyon)
        if tuketim is not None:
            print("\nTüketilen Değerler:")
            for makro, miktar in tuketim.items():
                print(f"{makro.capitalize()}: {miktar:.2f}")

            kalan_ihtiyaclar = kalan_ihtiyac_hesapla(ihtiyaclar, tuketim)
            print("\nKalan İhtiyaçlarınız:")
            for makro, miktar in kalan_ihtiyaclar.items():
                print(f"{makro.capitalize()}: {miktar:.2f}")

            oneriler = filtreleme_ve_oneri(dataset, saat, kalan_ihtiyaclar)
            print("\nÖnerilen Yemekler:")
            print(oneriler)
    else:
        print("Geçersiz seçim.")

    devam = input("Başka bir işlem yapmak istiyor musunuz? (evet/hayır): ").lower()
    if devam != "evet":
        break
