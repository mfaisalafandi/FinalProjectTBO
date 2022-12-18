import os

class CYK():
    # Fungsi yang akan dipanggil dalam class CYK, untuk mengatur assignment arrTabel dan pemanggilan fungsi
    def __init__(self, kata, init_grammar, init_vra):
        self.kata = kata
        self.init_grammar = init_grammar
        self.init_vra = init_vra
        print(init_grammar)
        # print(len(self.init_vra))
        # os.system("pause")
        self.sKata = self.__slicing()
        self.arrTabel = [[' ' for x in range(len(self.sKata)+1)] for y in range(len(self.sKata)+1)]
        self.__firstCal()
        self.__multiCal(1, len(self.sKata))
        # Menampilkan hasil string
        print(self.checkResult())

    def __slicing(self):
        kata = self.kata.split()
        return kata;

    # Fungsi untuk iterasi pertama, mengkalkulasi bottom row
    def __firstCal(self):
        print("\n\n")
        num = 0
        # Perulangan sebanyak jumlah karakter
        for k in self.sKata:
            num += 1
            Wi = set()
            # Perulangan sebanyak production
            for iV in self.init_vra:
                # print(iV)
                for key, value in iV.items():
                    InNew = set()
                    InNew.add(k.lower())
                    # print(set(value).intersection(InNew))
                    print(InNew, " <=> ", set(value), "\n =", set(value).intersection(InNew))
                    if set(value).intersection(InNew):
                        # print(key, "ketemu")
                        Wi.add(key)
            self.arrTabel[num][num] = Wi
        print("Calculating the Bottom ROW : ")
        self.__viewTabel()

    # Fungsi untuk mengatur kalkulasi top row
    def __multiCal(self, sum, lim):
        # Base case mengembalikan arrTabel yang sudah diisi
        if sum >= len(self.kata) or lim < 1:
            return 
        # Memanggil fungsi repeatCal untuk perulangan per baris
        self.__repeatCal(sum, lim)
        # Menjalankan secara rekursif untuk perulangan triangle tabel
        sum += 1
        lim -= 1
        return self.__multiCal(sum, lim)

    # Mengecek hasil cell Xi,j terakhir untuk mendapatkan string valid/tidak
    def checkResult(self):
        print(" => ", end="")
        if (self.arrTabel[1][len(self.sKata)]).intersection('K'):
            hasil = "=> String Valid <="
        else:
            hasil = "=> String Tidak Valid <="
        return hasil

    # Menampilkan triangular table
    def __viewTabel(self):
        for i in range(1, len(self.sKata) + 1):
            for j in range(i, len(self.sKata) + 1):
                print(i, end=",")
                print(j, end=" = ")
                print(self.arrTabel[i][j], end=" ")
            print(end="\n")
        print()

    # Mendapatkan variabel dan menggabungkanya menjadi 1 tuple
    def __getVariabel(self, sum, lim, i, j, k, l):
        Wi = set()
        # Memasukkan semua key dari transition dan menconcatenate
        for m in self.arrTabel[i][k]:
            for n in self.arrTabel[l][j]:
                gabung = [m, n]
                Wi.add(tuple(gabung))
        Y = set()
        for o in Wi:
            for key, value in self.init_grammar["Productions"].items():
                for m in value:
                    # print(tuple(o), " | ", tuple(m), " => ", set(o).intersection(m), " = ", key)
                    # formatM = str(m).split("'");
                    # strM = (formatM[1], formatM[3])
                    # print(str(o), " | ", str(strM), " => ", str(o) == str(strM), " = ", key)
                    # if o.issubset(m):
                    # if str(o) == str(strM):
                    if set(o).intersection(m):
                        Y.add(key)
        return Y

    # Mengatur perulangan sesuai rumus compare n pairs
    def __formulaCal(self, sum, lim, i, j):
        l = i
        Y = set()
        for k in range(i, j):
            l += 1
            # Menggabungkan production rule yang dituju 
            Y = Y.union(self.__getVariabel(sum, lim, i, j, k, l))
        self.arrTabel[i][j] = Y
        self.__viewTabel()

    # Fungsi untuk perulangan baris sepanjang lim untuk membentuk seperti segitiga
    def __repeatCal(self, sum, lim):
        for i in range(1, lim):
            j = i + sum
            self.__formulaCal(sum, lim, i, j)