def open_file(filepath):
    data = []
    with open(filepath, 'r') as file:
        raw = file.readlines()
        for rule in raw:
            data.append(rule.strip('\n'))
    return data

def raw_to_cfg(raw):
    cfg = []
    for line in raw:
        cfg.append(line.split(' -> '))
    for rule in cfg:
        rule[1] = set(rule[1].split(' | '))
    for rule in cfg:
        new_body = set()
        for element in rule[1]:
            element_to_tuple = tuple(element.split(' '))
            new_body.add(element_to_tuple)
        rule[1] = new_body
    return cfg
