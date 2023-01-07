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
        result, table = Obj_CNF.cek_result()
        if result == 1:
            return render_template('bahasa.html', st=request.form["kalimat"], result=result, Rtable=table, std=request.form["kalimat"].split(' '))
        else:
            return render_template('bahasa.html', st=request.form["kalimat"], result=result, Rtable=0)
    else:
        return render_template('bahasa.html', st="", result=0, Rtable=0)

app.run(debug=True)
