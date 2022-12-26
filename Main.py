from flask import Flask
from flask import request
from flask import render_template
import CNF as Mod_CNF;
import CFG as Mod_CFG;
    
# Membuka file cnf.txt dan memasukkannya ke dalam variabel tipe list
raw_cfg = Mod_CFG.open_file('cnf.txt')
cnf = Mod_CFG.raw_to_cfg(raw_cfg)
# Menggunakan modul flask untuk menampilkan aplikasi berbasis web
app = Flask(__name__, template_folder='templates')
# Link routing pertama kali aplikasi dibuka
@app.route('/')
def index():
    return render_template('index.html')
# Link routing ketika user mengklik link bahasa
@app.route('/bahasa/', methods=("POST", "GET"))
def bahasa():
    if (request.method == "POST") and (request.form["kalimat"] != ""):
        Obj_CNF = Mod_CNF.CNF(cnf, request.form["kalimat"].split(' '))
        result = Obj_CNF.cek_result()
        return render_template('bahasa.html', result=result, list=cnf)
    else:
        return render_template('bahasa.html', result=0, list=cnf)

app.run(debug=True)
