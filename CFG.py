# Membaca file dan memasukkan datanya pada list data
def open_file(filepath):
    data = []
    with open(filepath, 'r') as file:
        raw = file.readlines()
        for rule in raw:
            data.append(rule.strip('\n'))
    return data
# Memisahkan data pada file cnf.txt antara key dan body
def raw_to_cfg(raw):
    cfg = []
    for line in raw:
        # Memisahkan head & body dari rule cnf
        cfg.append(line.split(' -> '))
    for rule in cfg:
        # Memisahkan setiap rule dari body cnf
        rule[1] = set(rule[1].split('|'))
    for rule in cfg:
        new_body = set()
        for element in rule[1]:
            element_to_tuple = tuple(element.split(' '))
            new_body.add(element_to_tuple)
        rule[1] = new_body
    return cfg
    
