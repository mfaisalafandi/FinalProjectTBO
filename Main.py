import CYK as tabelFilling
import CNF as chom
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def get_gramar():
    init_vra = [
        {"Num": ["semua", "seorang", "ribuan", "lima", "seekor", "tiga", "ratusan", "tujuh ratus", "berpuluh-puluh", "beratus-ratus", "juta", "kedua", "berempat", "banyak", "belasan", "dua", "11", "3", "sepuluh", "25", "dua", "satu", "kedua", "5", "seikat", "setangkai", "sepasang", "10", "dua puluh", "empat", "separuh", "15", "2", "1", "7", "setengah", "8", "bertahun-tahun", "27", "delapan", "selusin", "berhari-hari"]},

        {"Noun": ["makalah", "kampus", "siswa", "bantuan", "gadis", "seseorang", "tali", "orang", "lapangan", "banteng", "orang-orang", "jalan", "serdadu", "bapak", "karcis", "eksemplar", "buku", "acara", "bedah", "mahasiswa", "masyarakat", "pasang", "mata", "pertandingan", "wasit", "bendera", "pinggir", "lapangan", "pemain", "ruangan", "tugas", "sepeda", "listrik", "jawaban", "papan tulis", "rapat umum", "sejoli", "pantai", "sapi", "ekor", "pensil", "buah", "apel", "ibu", "adik", "baju", "korban", "tsunami", "ayah", "motor", "paman", "istri", "unit", "laptop", "ban", "mobil", "rumah", "mangga", "kakak", "kakek", "telur", "ikat", "kangkung", "bayam", "sawah", "kilogram", "daging", "bunga", "mawar", "penjual", "ayam", "ikan", "mujair", "petak", "gorengan" , "meja", "kerja", "potong", "puding", "kambing", "wasit kedua", "tugas", "kuliah", "sisir", "pisang", "proposal", "berbulan-bulan", "atas", "meja", "ponsel", "kucing", "Mangga", "beras", "rapat" "daring", "kg", "sandal", "kucing", "ekor", "rumah", "hektar", "konglomerat", "manusia", "unit", "gula", "mobil", "galon", "air", "kantor", "gedung", "pembangunan", "tanaman", "kebun", "jenis", "objek", "kampungku", "jam", "sehari", "ember", "liter", "warung", "cangkir", "kopi", "video", "juta", "penonton", "kemarin", "dunia"]},

        {"Pronoun": ["saya", "itu", "kami", "pak", "si", "kakek", "oleh", "nenek"]},

        {"Adj": ["cantik", "lebar", "baru"]},

        {"Adv": ["sedang", "selalu", "sudah", "masih", "saja", "sekitar", "lagi", "hanya", "sekali", "telah"]},

        {"Verb": ["dikumpul", "mendapatkan", "bertemu", "menarik", "memadati", "menyeruduk", "menghampiri", "membeli", "dibagikan", "membantu", "menonton", "mengangkat", "memasuki", "mengerjakan", "mengendarai", "ditulis", "menghadiri", "bermain", "meninggal", "ada", "membeli", "mencuci", "menjual", "mempunyai", "memiliki", "mengganti", "merenovasi", "memakan", "menggoreng", "memasak", "memetik", "memelihara", "menebang", "meminjam", "menyembelih", "tersisa", "membawa", "makan", "tinggal", "diikuti", "dianjurkan", "minum", "tidur", "wisata", "selama", "memuat", "berkurban", "disaksikan"]},

        {"Prep": ["di", "pada", "untuk"]},

        {"PropNoun": ["tbo", "anto", "lita", "gunggus", "bhadrika", "salim", "ary", "eka", "saleh", "fredy", "andi", "kadir", "wawin", "surya", "mahayasa", "fika", "okta", "hutan lindung", "dede", "lohan", "rama", "bella", "nia", "widia", "budi", "alit", "faisal"]}
        # "Terminals": ["semua", "seorang", "ribuan", "lima", "seekor", "tiga", "ratusan", "tujuh ratus", "berpuluh-puluh", "beratus-ratus", "juta", "kedua", "berempat", "banyak", "belasan", "dua", "11", "3", "sepuluh", "25", "dua", "satu", "kedua", "5", "seikat", "setangkai", "sepasang", "10", "dua puluh", "empat", "separuh", "15", "2", "1", "7", "setengah", "8", "bertahun-tahun", "27", "delapan", "selusin", "berhari-hari", "makalah", "kampus", "siswa", "bantuan", "gadis", "seseorang", "tali", "orang", "lapangan", "banteng", "orang-orang", "jalan", "serdadu", "bapak", "karcis", "eksemplar", "buku", "acara", "bedah", "mahasiswa", "masyarakat", "pasang", "mata", "pertandingan", "wasit", "bendera", "pinggir", "lapangan", "pemain", "ruangan", "tugas", "sepeda", "listrik", "jawaban", "papan tulis", "rapat umum", "sejoli", "pantai", "sapi", "ekor", "pensil", "buah", "apel", "ibu", "adik", "baju", "korban", "tsunami", "ayah", "motor", "paman", "istri", "unit", "laptop", "ban", "mobil", "rumah", "mangga", "kakak", "kakek", "telur", "ikat", "kangkung", "bayam", "sawah", "kilogram", "daging", "bunga", "mawar", "penjual", "ayam", "ikan", "mujair", "petak", "gorengan" , "meja", "kerja", "potong", "puding", "kambing", "wasit kedua", "tugas", "kuliah", "sisir", "pisang", "proposal", "berbulan-bulan", "atas", "meja", "ponsel", "kucing", "Mangga", "beras", "rapat" "daring", "kg", "sandal", "kucing", "ekor", "rumah", "hektar", "konglomerat", "manusia", "unit", "gula", "mobil", "galon", "air", "kantor", "gedung", "pembangunan", "tanaman", "kebun", "jenis", "objek", "kampungku", "jam", "sehari", "ember", "liter", "warung", "cangkir", "kopi", "video", "juta", "penonton", "kemarin", "dunia", "saya", "itu", "kami", "orang", "Pak", "si", "Kakek", "oleh", "Nenek", "cantik", "lebar", "baru", "sedang", "selalu", "sudah", "masih", "saja", "sekitar", "lagi", "hanya", "sekali", "telah", "dikumpul", "mendapatkan", "bertemu", "menarik", "memadati", "menyeruduk", "menghampiri", "membeli", "dibagikan", "membantu", "menonton", "mengangkat", "memasuki", "mengerjakan", "mengendarai", "ditulis", "menghadiri", "bermain", "meninggal", "ada", "membeli", "mencuci", "menjual", "mempunyai", "memiliki", "mengganti", "merenovasi", "memakan", "menggoreng", "memasak", "memetik", "memelihara", "menebang", "meminjam", "menyembelih", "tersisa", "membawa", "makan", "tinggal", "diikuti", "dianjurkan", "minum", "tidur", "wisata", "selama", "memuat", "berkurban", "disaksikan", "di", "pada", "untuk", "TBO", "Anto", "Lita", "Gunggus", "Bhadrika", "salim", "Ary", "Eka", "Saleh", "Fredy", "Andi", "Kadir", "Wawin", "Surya", "Mahayasa", "Fika", "Okta", "Hutan Lindung", "dede", "lohan", "Rama", "Bella", "Nia", "Widia", "Budi", "Alit", "Faisal"],
    ]
    init_gramar = {
        "Variables": ["K", "S", "P", "O", "Pel", "Ket", "NP", "VP", "NumP", "PP", "Adj", "Adv", "PropNoun", "Pronoun", "Noun", "Prep", "Num", "Verb"],
        "Terminals": [""],
        "Productions": [
            {"head": "K", "body": ["S", "P", "Ket"]},
            {"head": "K", "body": ["S", "P", "O"]},
            {"head": "K", "body": ["S", "P", "O", "Ket"]},
            {"head": "K", "body": ["S", "P"]},
            {"head": "K", "body": ["S", "P", "Pel"]},
            {"head": "S", "body": ["NP"]},
            {"head": "P", "body": ["VP"]},
            {"head": "P", "body": ["NumP"]},
            {"head": "O", "body": ["NP"]},
            {"head": "Ket", "body": ["NP"]},
            {"head": "Ket", "body": ["PP"]},
            {"head": "Pel", "body": ["NP"]},
            {"head": "Pel", "body": ["PP"]},
            {"head": "NP", "body": ["NumP", "NP"]},
            {"head": "NP", "body": ["NP", "PP"]},
            {"head": "NP", "body": ["NP", "PropNoun"]},
            {"head": "NP", "body": ["NP", "Adv"]},
            {"head": "NP", "body": ["NP", "Adj"]},
            {"head": "NP", "body": ["NP", "Pronoun"]},
            {"head": "NP", "body": ["NP", "Noun"]},
            {"head": "NP", "body": ["Pronoun"]},
            {"head": "NP", "body": ["Noun"]},
            {"head": "PP", "body": ["Prep", "NP"]},
            {"head": "NumP", "body": ["Num", "Noun"]},
            {"head": "NumP", "body": ["Adv", "Num"]},
            {"head": "NumP", "body": ["Num"]},
            {"head": "VP", "body": ["Adv", "VP"]},
            {"head": "VP", "body": ["Adv", "Verb"]},
            {"head": "VP", "body": ["Verb"]},
        ],
        "Start": "K"
    }
    chomsky = chom.CNF(init_gramar)
    init_gramar = chomsky.conversion()
    return init_gramar, init_vra

def Main():
    init_gramar, init_vra = get_gramar()

    window = tk.Tk()
    window.configure(bg="white")
    window.geometry("500x300")
    window.resizable(False, False)
    window.title("Kelompok 2 | KBBI Bahasa Indonesia")

    kata = tk.StringVar()

    input_frame = ttk.Frame(window)
    input_frame.pack(padx=10, pady=10, fill="x", expand=True)

    kalimat_label = ttk.Label(input_frame, text="Masukkan Kalimat: ")
    kalimat_label.pack(padx=10, pady=5, expand=True)

    kalimat_input = ttk.Entry(input_frame, textvariable=kata)
    kalimat_input.pack(padx=10, pady=5, fill="x", expand=True)

    def btn_click():
        # print(str(kata.get()))
        Obj = tabelFilling.CYK(str(kata.get()), init_gramar, init_vra)
        hasil = Obj.checkResult()
        kalimat_hasil = ttk.Label(input_frame, text=hasil)
        kalimat_hasil.pack(padx=10, pady=5, expand=True)

    btn_input = ttk.Button(input_frame, text="Cek!", command=btn_click)
    btn_input.pack(fill="x", expand=True, padx=10, pady=5)

    window.mainloop()

Main()