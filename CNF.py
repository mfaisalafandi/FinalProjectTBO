class CNF:
    def __init__(self, cnf, words):
        self.LWords = words
        self.empty = '\u2205'
        self.cnf = cnf
        self.table = self.create_table()
        self.filling_bottom()
        self.filling_all(1)

    # Mengecek hasil apakah kalimat diterima/tidak
    def cek_result(self):
        print("\n",self.table[len(self.table) - 1][0])
        if 'K' in self.table[len(self.table) - 1][0]:
            # Final CYK tabel filling terdapat key K, return 1(valid) & hasil tabel
            return 1, self.table
        else:
            return -1, self.table
    
    # Membuat tabel dengan baris & kolom sebanyak jumlah kata
    def create_table(self):
        table = []
        for i in range(len(self.LWords)):
            table.append([])
            for j in range(len(self.LWords)):
                if i >= j:
                    # Baris & kolom digunakan
                    table[i].append(set())
                else:
                    # Baris & kolom tidak digunakan
                    table[i].append(' ')
        return table

    # Mengisi bagian bawah tabel filling
    def filling_bottom(self):
        # Melakukan perulangan sebanyak kata
        for i, word in enumerate(self.LWords):
            place = set()
            # Perulangan pada rule CNF
            for row in self.cnf:
                # Perulangan bagian terkecil rule body pada CNF
                for element in row[1]:
                    # Jika kata terdapat pada rule cnf
                    if (word in element) or (word.lower() in element) or (word.capitalize() in element):
                        # Masukkan key dimana kata terdapat pada rule
                        place.add(row[0])
                        break
            self.table[i][i] = place

    # Mengisi secara keseluruhan table
    def filling_all(self, row):
        # Jika kolom pertama di baris terakhir != set() kosong, maka tampilkan hasil CYK
        if self.table[len(self.table) - 1][0] != set():
            return
        # Mengisi baris selanjutnya
        next_row = self.iteration(row)
        self.filling_all(next_row)

    # Mengisi baris dari tabel
    def iteration(self, row):
        # perulangan menurun dari kolom yang dimaksud hingga bawah tabel
        for column in range(len(self.table) - 1, -1, -1):
            # Jika baris & kolom tersebut kosong
            if self.table[row][column] == set():

                list_product = []
                # Perulangan dari kolom row saat tersebut
                for i in range(0, row):
                    if self.table[i][column] == self.empty:
                        list_product.append(set())
                    elif self.table[i][column] != ' ' and self.table[i][column] != set():
                        list_product.append(self.table[i][column])

                # Perulangan dari baris row saat tersebut
                for i in range(column + 1, len(self.table)):
                    if self.table[row][i] == self.empty:
                        list_product.append(set())
                    elif self.table[row][i] != ' ' and self.table[row][i] != set():
                        list_product.append(self.table[row][i])
                # Kedua perulangan di atas akan mendapatkan data yang sudah tersusun dari tabel
                # Sehingga tidak perlu dilakukan union, hanya kombinasi/concatenat

                result_list = self.make_combination(list_product)
                combine_result = self.changeTipe(result_list)
                
                self.table[row][column] = self.find_cnf(combine_result)

                row = (row + 1) if row + 1 < len(self.table) else 1
                return row
        # Tambahkan baris jika jumlah baris berikutnya < dari total semua baris, selain itu kembali ke baris nomor 1
        row = (row + 1) if row + 1 < len(self.table) else 1
        return row

    # Melakukan kombinasi key
    def make_combination(self, list_input):
        # Membagi data key yang didapat menjadi 2,
        count = len(list_input) // 2
        combination = []
        for i in range(count):
            # sehingga pada bagian kiri dapat dijadikan sebagai i, bagian kanan sebagai j
            list1 = list_input[i]
            list2 = list_input[i + count]
            combination.append([])
            for element1 in list1:
                for element2 in list2:
                    # Melakukan kombinasi
                    combination[i].append(tuple((element1, element2)))
        return combination

    # Mengubah list ke set
    def changeTipe(self, combination):
        result_set = set()
        for x in combination:
            for y in x:
                result_set.add(y)
        return result_set

    # Mencari cnf berdasarkan produk
    def find_cnf(self, combine):
        cnf_key = set()
        for com in combine:
            for row in self.cnf:
                # Jika hasil kombinasi terdapat pada body rule cnf,
                if com in row[1]:
                    # masukkan key rule cnf
                    cnf_key.add(row[0])
        if cnf_key != set():
            return cnf_key
        else:
            return self.empty
