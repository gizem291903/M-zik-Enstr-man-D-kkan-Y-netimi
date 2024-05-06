import sqlite3
import tkinter as tk
from tkinter import messagebox
import random


class Enstruman:
    def __init__(self, root, conn, c):
        self.root = root
        self.conn = conn
        self.c = c

        self.adi = tk.StringVar()
        self.stok_miktari = tk.IntVar()
        self.fiyat = tk.DoubleVar()

        self.enstruman_adi_etiket = tk.Label(root, text="Enstrüman Adı:")
        self.enstruman_adi_etiket.grid(row=0, column=0)
        self.enstruman_adi_giris = tk.Entry(root, textvariable=self.adi)
        self.enstruman_adi_giris.grid(row=0, column=1)

        self.stok_etiket = tk.Label(root, text="Stok Miktarı:")
        self.stok_etiket.grid(row=1, column=0)
        self.stok_giris = tk.Entry(root, textvariable=self.stok_miktari)
        self.stok_giris.grid(row=1, column=1)

        self.fiyat_etiket = tk.Label(root, text="Fiyat (TL):")
        self.fiyat_etiket.grid(row=2, column=0)
        self.fiyat_giris = tk.Entry(root, textvariable=self.fiyat)
        self.fiyat_giris.grid(row=2, column=1)

        self.ekle_dugme = tk.Button(root, text="Enstrüman Ekle", command=self.enstruman_ekle)
        self.ekle_dugme.grid(row=3, columnspan=2)

        self.enstruman_listesi = tk.Listbox(root, width=50, height=10)
        self.enstruman_listesi.grid(row=5, columnspan=2)

        self.enstrumanlari_getir()

    def enstruman_ekle(self):
        adi = self.adi.get()
        stok_miktari = self.stok_miktari.get()
        fiyat = self.fiyat.get()

        self.c.execute("INSERT INTO Enstruman (adi, stok_miktari, fiyat) VALUES (?, ?, ?)", (adi, stok_miktari, fiyat))
        self.conn.commit()
        messagebox.showinfo("Başarılı", "Enstrüman başarıyla eklendi.")

        self.enstrumanlari_getir()

    def enstrumanlari_getir(self):
        self.enstruman_listesi.delete(0, tk.END)
        self.c.execute("SELECT * FROM Enstruman")
        enstrumanlar = self.c.fetchall()
        for enstruman in enstrumanlar:
            self.enstruman_listesi.insert(tk.END, f"{enstruman[1]} - Stok: {enstruman[2]} - Fiyat: {enstruman[3]} TL")


class Musteri:
    def __init__(self, root, conn, c):
        self.root = root
        self.conn = conn
        self.c = c

        self.musteri_listesi = tk.Listbox(root, width=50, height=10)
        self.musteri_listesi.grid(row=7, columnspan=2)
        self.musteri_listesi.bind('<Double-Button-1>', self.musteriye_tiklandi)

        self.musterileri_getir()

    def musterileri_getir(self):
        self.musteri_listesi.delete(0, tk.END)
        self.c.execute("SELECT * FROM Musteri")
        musteriler = self.c.fetchall()
        for musteri in musteriler:
            self.musteri_listesi.insert(tk.END, f"ID: {musteri[0]} - {musteri[1]} {musteri[2]} - Telefon: {musteri[3]}")

    def musteriye_tiklandi(self, event):
        secilen_musteri = self.musteri_listesi.curselection()[0]
        musteri_id = self.musteri_listesi.get(secilen_musteri).split()[1]
        self.root.destroy()  # Önceki pencereyi kapat
        musteri_pencere = tk.Tk()  # Yeni pencere oluştur
        musteri_pencere.title("Müşteri Sipariş Geçmişi")

        # Seçilen müşteriye ait sipariş geçmişi burada gösterilecek
        # Müşteri ID'sini kullanarak veritabanından sorgu yapılabilir.

        musteri_pencere.mainloop()


class Satis:
    def __init__(self, root, conn, c, enstruman):
        self.root = root
        self.conn = conn
        self.c = c
        self.enstruman = enstruman
        self.musteri_id = tk.StringVar()  # Musteri ID'si için bir StringVar tanımlıyoruz

        self.enstruman_secim = tk.StringVar()
        self.musteri_secim = tk.StringVar()

        self.enstruman_etiket = tk.Label(root, text="Satılacak Enstrüman:")
        self.enstruman_etiket.grid(row=8, column=0)
        self.enstruman_giris = tk.Entry(root, textvariable=self.enstruman_secim)
        self.enstruman_giris.grid(row=8, column=1)

        self.musteri_etiket = tk.Label(root, text="Müşteri ID:")
        self.musteri_etiket.grid(row=9, column=0)
        self.musteri_giris = tk.Entry(root,
                                      textvariable=self.musteri_id)  # Musteri ID'si için giriş kutusu değişkenini değiştiriyoruz
        self.musteri_giris.grid(row=9, column=1)

        self.satis_dugme = tk.Button(root, text="Satış Yap", command=self.satıs_yap)
        self.satis_dugme.grid(row=10, columnspan=2)

    def satıs_yap(self):
        enstruman_adi = self.enstruman_secim.get()
        musteri_id = int(self.musteri_id.get())  # Değişiklik: self.musteri_id'yi getiriyoruz

        self.c.execute("SELECT * FROM Enstruman WHERE adi=?", (enstruman_adi,))
        enstruman = self.c.fetchone()

        if enstruman:
            if enstruman[2] > 0:
                siparis_no = random.randint(1000, 9999)
                self.c.execute("INSERT INTO Satis (siparis_no, enstruman_id, musteri_id) VALUES (?, ?, ?)",
                               (siparis_no, enstruman[0], musteri_id))
                self.conn.commit()
                messagebox.showinfo("Başarılı", "Satış başarıyla gerçekleştirildi.")

                self.c.execute("UPDATE Enstruman SET stok_miktari = ? WHERE adi = ?", (enstruman[2] - 1, enstruman_adi))
                self.conn.commit()
            else:
                messagebox.showerror("Hata", "Stokta bu enstrümandan kalmamış.")
        else:
            messagebox.showerror("Hata", "Böyle bir enstrüman bulunamadı.")

        self.enstruman.enstrumanlari_getir()  # Enstruman listesini güncelle


class Destek:
    def __init__(self, root, conn, c):
        self.root = root
        self.conn = conn
        self.c = c

        self.talep_no = tk.IntVar()
        self.talep_detaylari = tk.StringVar()

        self.talep_no_etiket = tk.Label(root, text="Talep Numarası:")
        self.talep_no_etiket.grid(row=11, column=0)
        self.talep_no_giris = tk.Entry(root, textvariable=self.talep_no)
        self.talep_no_giris.grid(row=11, column=1)

        self.talep_detaylari_etiket = tk.Label(root, text="Talep Detayları:")
        self.talep_detaylari_etiket.grid(row=12, column=0)
        self.talep_detaylari_giris = tk.Entry(root, textvariable=self.talep_detaylari)
        self.talep_detaylari_giris.grid(row=12, column=1)

        self.destek_dugme = tk.Button(root, text="Talep Oluştur", command=self.destek_olustur)
        self.destek_dugme.grid(row=13, columnspan=2)

    def destek_olustur(self):
        talep_no = self.talep_no.get()
        talep_detaylari = self.talep_detaylari.get()

        self.c.execute("INSERT INTO Destek (talep_no, talep_detaylari) VALUES (?, ?)", (talep_no, talep_detaylari))
        self.conn.commit()
        messagebox.showinfo("Başarılı", "Destek talebi oluşturuldu.")


class MuzikDukkaniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Müzik Enstrümanları Dükkanı")

        self.conn = sqlite3.connect('muzik_dukkani.db')
        self.c = self.conn.cursor()

        self.enstruman = Enstruman(root, self.conn, self.c)
        self.musteri = Musteri(root, self.conn, self.c)
        self.satis = Satis(root, self.conn, self.c, self.enstruman)
        self.destek = Destek(root, self.conn, self.c)

        self.kilavuz_buton = tk.Button(root, text="Kullanım Kılavuzu", command=self.kilavuz_goster)
        self.kilavuz_buton.grid(row=15, columnspan=2)

    def kilavuz_goster(self):
        # Kullanım kılavuzu metnini gösteren bir pencere aç
        kilavuz_pencere = tk.Toplevel(self.root)
        kilavuz_pencere.title("Kullanım Kılavuzu")

        # Kullanım kılavuzu metni
        metin = """
        Kullanım Kılavuzu:

        1. Enstrüman Ekle:
           - Enstrüman Adı, Stok Miktarı ve Fiyatını girerek "Enstrüman Ekle" düğmesine basın.

        2. Müşteri Listesi:
           - Müşteri listesini görmek için müşteri sekmesine tıklayın.
           - İlgili müşterinin üzerine çift tıklayarak müşteriye ait sipariş geçmişini görebilirsiniz.

        3. Satış Yap:
           - Satılacak enstrümanı seçin ve müşteri ID'sini girin.
           - "Satış Yap" düğmesine tıklayarak satışı gerçekleştirin.

        4. Destek Talebi Oluştur:
           - Talep Numarası ve Detaylarını girerek "Talep Oluştur" düğmesine basın.

        5. Kullanım Kılavuzu:
           - Uygulama hakkında daha fazla bilgi almak için "Kullanım Kılavuzu" düğmesine basın.
        """

        # Metni etikete ekleyerek pencereye yerleştir
        etiket = tk.Label(kilavuz_pencere, text=metin, justify=tk.LEFT)
        etiket.pack()


root = tk.Tk()
app = MuzikDukkaniApp(root)
root.mainloop()
