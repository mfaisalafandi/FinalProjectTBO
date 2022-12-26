class CNF:
    def __init__(self, cnf, words):
        self.LWords = words
        self.empty = '\u2205'
        self.cnf = cnf
        self.table = self.create_table()
        self.filling_bottom()
        self.filling_all(1)

    def create_table(self):
        table = []
        for i in range(len(self.LWords)):
            table.append([])
            for j in range(len(self.LWords)):
                if i < j:
                    table[i].append(' ')
                else:
                    table[i].append(set())
        return table

    def filling_bottom(self):
        for i, word in enumerate(self.LWords):
            cell = set()
            for row in self.cnf:
                for element in row[1]:
                    if (word in element) or (word.lower() in element) or (word.capitalize() in element):
                        print(element)
                        cell.add(row[0])
                        break
            self.table[i][i] = cell
        print(self.table)

    def filling_all(self, row):
        if self.table[len(self.table) - 1][0] != set():
            if 'K' in self.table[len(self.table) - 1][0]:
                print("Success")
            else:
                print("Error")
            return
        next_row = self.iteration(row)
        self.filling_all(next_row)

    def iteration(self, row):
        for column in range(len(self.table) - 1, -1, -1):
            if self.table[row][column] == set():

                list_of_intersect = []
                for i in range(0, row):
                    if self.table[i][column] == self.empty:
                        list_of_intersect.append(set())
                    elif self.table[i][column] != ' ' and self.table[i][column] != set():
                        list_of_intersect.append(self.table[i][column])

                for i in range(column + 1, len(self.table)):
                    if self.table[row][i] == self.empty:
                        list_of_intersect.append(set())
                    elif self.table[row][i] != ' ' and self.table[row][i] != set():
                        list_of_intersect.append(self.table[row][i])

                result_list = self.make_combination(list_of_intersect)
                combine_result = self.combine(result_list)
                
                self.table[row][column] = self.find_cnf(combine_result)
                row = (row + 1) if row + 1 < len(self.table) else 1
                return row
        row = (row + 1) if row + 1 < len(self.table) else 1
        return row

    def make_combination(self, list_input):
        count = len(list_input) // 2
        combination = []
        for i in range(count):
            list1 = list_input[i]
            list2 = list_input[i + count]
            combination.append([])
            for element1 in list1:
                for element2 in list2:
                    combination[i].append(tuple((element1, element2)))
        return combination

    def combine(self, raw_combination):
        result_set = set()
        for x in raw_combination:
            # print("X = ", x)
            for y in x:
                # print("Y => ", y)
                result_set.add(y)
        return result_set

    def find_cnf(self, combine):
        cnf_return = set()
        for com in combine:
            for row in self.cnf:
                if com in row[1]:
                    print(row[0], com)
                    cnf_return.add(row[0])
        if cnf_return == set():
            return self.empty
        else:
            return cnf_return

    def cek_result(self):
        print("\n",self.table[len(self.table) - 1][0])
        if 'K' in self.table[len(self.table) - 1][0]:
            return 1
        else:
            return -1
