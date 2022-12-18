import os
import itertools

from CFG import CFG

# Class yang merepresentasikan CNF
class CNF(CFG):
    def __init__(self, init_gramar):
        # membuat objek CFG dan interpretasi dari tupple
        # generate_steps: Boolean menunjukkan apakah konstruktor harus membuat file keluaran dengan semua langkah yang diperlukan untuk mengonversi ke bentuk normal Chomsky. True menghasilkan file, False tidak.
        
        # Membangun CNF sesuai dengan class CFG.
        # super() digunakan untuk mengacu ke kelas induk dari suatu objek.
        super().__init__(init_gramar)
        self.var_count = 1 # Digunakan untuk membedakan variabel T => T1, T2, ...
        
        # Langkah-langkah yang diperlukan untuk mencapai bentuk Chomsky Normal Form
        self.__eliminate_epsilon_transitions()
        self.__eliminate_unit_productions()
        # self.__eliminate_useless_symbols()
        self.__arrange_variable_bodies()
        self.__break_long_bodies()
        
    def __write_step(self, step_description):
        # Tidak ada file keluaran dan tidak ada yang bisa dilakukan.
        print(step_description)
        # mencetak variabel, terminal
        vars_str = 'variables: ' + str(self.variables)
        term_str = 'terminals: ' + str(self.terminals)
        prod_str = 'productions:\n'
        print(vars_str)
        print(term_str)
        print(prod_str)

        for key, value in self.productions.items():
            for rule in value:
                line = key + ' => ' + str(rule)
                print(line)
        print()

    def __eliminate_epsilon_transitions(self):
        # Hilangkan Null Production
        nullables = self.__find_nullables()

        for key in self.productions:
            for rule in self.productions[key].copy():
                if(any(symbol in nullables for symbol in rule)):
                    unaffected = list(s for s in rule if s not in nullables)
                    powerset   = self.__get_powerset(rule)
                    new_rules  = set()
                    for n_rule in (x for x in powerset if len(x) > 0):
                        if (all(u in n_rule for u in unaffected)):
                            new_rules.add(n_rule)

                    # Add these newly generated rules.
                    self.productions[key].update(new_rules)

                elif len(rule) == 0:
                    # This case deletes the rule of the form A => Ɛ
                    self.productions[key].remove(rule)

        self.__write_step("Remove Null Production")
                
    def __eliminate_unit_productions(self):
        # Menghilangkan Unit Production
        pasangan_unit = [(var, var) for var in self.variables]
        new_productions = dict()

        # Membuat banyak pasangan dari satuan yang dasar
        for pasang in pasangan_unit:
            first  = pasang[0]
            second = pasang[1]
            rules  = self.productions.get(second, [])
            for s in rules:
                if len(s) == 1 and s[0] in self.variables:
                    pasangan_unit.append((first, s[0]))

        # Ulangi pengecekan pasangan unit untuk membuat produksi baru dengan menghilangkan unit production
        for pasang in pasangan_unit:
            first  = pasang[0]
            second = pasang[1]
            if second not in new_productions:
                new_productions[second] = set()

            for rule in self.productions.get(second, []):
                if len(rule) == 1 and rule[0] in self.variables:
                    # Mengatasi penulisan unit production berulang
                    continue
                new_productions[first].add(rule)

        # Mengganti production dengan yang baru tanpa unit production
        self.productions = new_productions
        self.__write_step("Remove Unit Production")

    def __eliminate_useless_symbols(self):
        # Hilangkan semua simbol yang tidak berguna. (variabel yang tidak pernah mengarah ke terminal mana pun dan simbol yang tidak dapat dijangkau dari simbol awal dengan aturan produksi saat ini).
        self.__eliminate_non_generating()
        self.__eliminate_non_reachable()
        self.__write_step('Remove Useless Symbol')

    def __eliminate_non_generating(self):
        # Hilangkan semua variabel yang tidak pernah mengarah ke terminal mana pun.
        non_generating = self.__find_non_generating()
        for var in non_generating:
            # Hapus semua aturan untuk variabel var
            self.productions.pop(var, None)
            for key in self.productions.copy():
                for rule in self.productions[key].copy():
                    if var in rule: self.productions[key].remove(rule)
            self.variables.remove(var)

    def __eliminate_non_reachable(self):
        # Hilangkan semua simbol yang tidak dapat dijangkau dari simbol awal
        non_reachables = self.__find_non_reachable()
        for s in non_reachables:
            # Hapus semua aturan untuk simbol ini (jika ada)
            self.productions.pop(s, None)
            for key in self.productions.copy():
                for rule in self.productions[key].copy():
                    if s in rule: self.productions[key].remove(rule)

            # Menghapus simbol dari set
            if s in self.variables:
                self.variables.remove(s)
            elif s in self.terminals:
                self.terminals.remove(s)

    def __arrange_variable_bodies(self):
        # Mengganti terminal yang panjang dengan 1 variabel yang baru dibuat.
        seen_terminals = dict()
        for key, value in self.productions.copy().items():
            for rule in value:
                if len(rule) > 1 and (any(r in self.terminals for r in rule)):
                    rule_2 = list(rule)
                    for symbol in rule_2:
                        if symbol in self.terminals :
                            new_var = "T" + str(self.var_count)
                            # Dalam kasus khusus, variabel sudah ada
                            while new_var in self.variables:
                                self.var_count += 1
                                new_var = "T" + str(self.var_count)

                            if symbol not in seen_terminals:
                                self.var_count += 1
                                self.variables.add(new_var)
                                seen_terminals[symbol] = new_var

                    for key2, value2 in seen_terminals.items():
                        self.productions[value2] = (key2,)

                    modified_rule = [seen_terminals.get(x, x) for x in rule_2]
                    modified_rule = tuple(modified_rule)
                    self.productions[key].remove(rule)
                    self.productions[key].add(modified_rule)
                    # print(type(self.productions[key]))

        self.__write_step("Membuat Terminal Baru")

    def __break_long_bodies(self):
        # Membuat badan production dengan 2 Terminal
        for key, value in self.productions.copy().items():
            for rule in value:
                # print(rule)
                # print(value)
                # print("lenR => ", len(rule))
                # print("lenV => ", len(value))
                if len(rule) > 2:
                    var_list = list(rule)
                    # print("cek => ", self.terminals)
                    # print("cek => ", self.variables)
                    if (all( symbol in self.variables for symbol in rule) == 0):
                        if (all( symbol in self.terminals for symbol in rule) == 0):
                            # print("Sama")
                            break;
                    # print("rule => ", rule)
                    # print("varL => ", var_list)

                    left_var = key
                    while len(var_list) >= 2:
                        new_var = "T" + str(self.var_count)
                        # Dalam kasus khusus, variabel sudah ada
                        while new_var in self.variables:
                            self.var_count += 1
                            new_var         = "T" + str(self.var_count)

                        if len(var_list) > 2:
                            self.var_count += 1
                            self.variables.add(new_var)
                            body = (var_list[0], new_var)
                            
                        elif len(var_list) == 2:
                            body = (var_list[0], var_list[1])
                        if left_var not in self.productions:
                            self.productions[left_var] = set()

                        # print(type(body), body)
                        # self.productions[left_var] = set(self.productions[left_var])
                        # print(type(self.productions[left_var]), self.productions[left_var], body)
                        self.productions[left_var].add(body)
                        # Memisahkan production
                        left_var = new_var
                        var_list = var_list[1:]

                    # x = set(self.productions[key])
                    # x.remove(rule)
                    self.productions[key].remove(rule)
                    
        self.__write_step('Membuat badan production dengan 2 Terminal')

    def __find_nullables(self):
        nullables = []
        # Temukan semua variabel dengan transisi epsilon
        for key, value in self.productions.items():
            # Jika ditemukan transisi epsilon
            if(any(len(rule) == 0 for rule in value)):
                nullables.append(key)

        if len(nullables) == 0:
            return []
        
        for key, value in self.productions.items():
            for rule in value:
                if all(s in nullables for s in rule):
                    nullables.append(key)

        return nullables
    
    def __find_non_generating(self):
        non_generating = []
        for var in self.variables:
            # Variabel tanpa aturan yang menghasilkan apa pun
            if var not in self.productions:
                non_generating.append(var)

        for key, value in self.productions.items():
            generating = False
            for rule in value:
                # Jika aturan berisi semua simbol pembangkit
                if (all(r not in non_generating for r in rule)):
                    generating = True
            if generating is False:
                non_generating.append(key)
        return non_generating

    def __find_non_reachable(self):
        reachables = [self.start]
        # Iteratively calculate all reachables
        for r in reachables:
            rules = {}
            if r in self.variables:
                rules = self.productions[r]
            for rule in rules:
                for symbol in rule:
                    if symbol not in reachables: reachables.append(symbol)

        all_symbols = set().union(self.variables, self.terminals)
        # Return difference between the two.
        return all_symbols - set(reachables)
                
    def __get_powerset(self, iterable):
        # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        chain = itertools.chain.from_iterable(itertools.combinations(s, r)
        for r in range(len(s)+1))
        return list(chain)
                            
    def conversion(self):
        # Tulis tata bahasa dalam bentuk normal Chomsky ke file json dalam format yang digunakan di seluruh proyek ini.
        init_grammar = dict()
        init_grammar["Variables"]   = list(self.variables)
        init_grammar["Terminals"]   = list(self.terminals)
        list_productions    = dict()
        # Ubah produksi menjadi daftar daftar
        for key, value in self.productions.items():
            print(key, value)
            tipe = str(type(value))
            # print(value, tipe.split("'")[1])
            if tipe.split("'")[1] == 'set':
                list_value            = [list(i) for i in value]
                list_productions[key] = list_value
            elif tipe.split("'")[1] == 'tuple':
                tipe2 = str(value) + "\n"
                print(tipe2.split("'")[1])
                list_productions[key] = [[tipe2.split("'")[1]]]
        
        init_grammar["Productions"] = list_productions
        init_grammar["Start"]       = self.start

        prod_str = '\nproductions:'
        print(prod_str, self.productions)
        print(prod_str, list_productions)

        # for key, value in self.productions.items():
        #     for rule in value:
        #         line = key + ' => ' + str(rule)
        #         print(line)
        # print()
        return init_grammar
        