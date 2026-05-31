otopark = {"1": [], "2": [], "3": []}
KAPASITE = 5
VERI_DOSYASI = "otopark_veri.txt"
RAPOR_DOSYASI = "gun_sonu_raporu.txt"


def verileri_yukle():
    """Program başlarken araçları dosyadan yükler."""
    try:
        dosya = open(VERI_DOSYASI, "r", encoding="utf-8")
        for satir in dosya:
            satir = satir.strip()
            if satir and ":" in satir:
                kat, araclar_str = satir.split(":")
                if araclar_str:
                    otopark[kat] = araclar_str.split(",")
                else:
                    otopark[kat] = []
        dosya.close()  
    except FileNotFoundError:
        
        pass


def verileri_kaydet():
    """Otoparkın güncel durumunu dosyaya kaydeder."""
    dosya = open(VERI_DOSYASI, "w", encoding="utf-8")
    for kat, araclar in otopark.items():
        araclar_str = ",".join(araclar)
        dosya.write(f"{kat}:{araclar_str}\n")
    dosya.close() 


def tum_araclar():
    return [plaka for kat_listesi in otopark.values() for plaka in kat_listesi]


def durum_goster():
    print("\n--- OTOPARK DURUMU ---")
    for kat, araclar in otopark.items():
        print(f"Kat {kat}: {len(araclar)}/{KAPASITE}")


def arac_giris(plaka, kat_no):
    if plaka in tum_araclar():
        return f"HATA: {plaka} zaten içeride!"

    if kat_no not in otopark:
        return "HATA: Geçersiz kat numarası!"

    if len(otopark[kat_no]) >= KAPASITE:
        return f"HATA: {kat_no}. kat dolu!"

    otopark[kat_no].append(plaka)
    verileri_kaydet()
    return f"{plaka} başarıyla {kat_no}. kata park edildi."


def arac_cikis(plaka):
    for kat, araclar in otopark.items():
        if plaka in araclar:
            araclar.remove(plaka)
            verileri_kaydet()
            return f"{plaka}, {kat}. kattan çıkış yaptı."
    return "HATA: Bu plakaya ait bir araç bulunamadı!"



verileri_yukle()

while True:
    durum_goster()
    islem = input(
        "İşlem seçiniz (giriş/çıkış/kapat/gün sonu): "
    ).lower()

    if islem == "kapat":
        print("Sistem verileriniz korunarak kapatıldı.")
        break

    if islem == "gün sonu":
        print("\n--- GÜN SONU RAPORU ---")

        rapor_dosyasi = open(RAPOR_DOSYASI, "a", encoding="utf-8")
        rapor_dosyasi.write("\n=== GÜN SONU RAPORU ===\n")

        for kat, araclar in otopark.items():
            arac_listesi = ", ".join(araclar) if araclar else "Boş"
            satir = f"Kat {kat} ({len(araclar)} araç): {arac_listesi}\n"
            print(satir, end="")
            rapor_dosyasi.write(satir)

            araclar.clear() 

        rapor_dosyasi.write("========================\n")
        rapor_dosyasi.close()  

        verileri_kaydet() 
        print(
            f"\nTüm kayıtlar sıfırlandı ve '{RAPOR_DOSYASI}' dosyasına raporlandı."
        )
        break

    if islem not in ["giriş", "çıkış"]:
        print("Geçersiz işlem!")
        continue

    plaka = input("Araç plakasını giriniz: ").upper().strip()

    if islem == "giriş":
        kat_no = input("Giriş yapılacak kat (1, 2, 3): ").strip()
        mesaj = arac_giris(plaka, kat_no)
        print(mesaj)

    elif islem == "çıkış":
        mesaj = arac_cikis(plaka)
        print(mesaj)