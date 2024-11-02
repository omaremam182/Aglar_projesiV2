from flask import Flask , render_template
from Forms import *
import firebase_admin
from firebase_admin import credentials


app = Flask (__name__)
app.config["SECRET_KEY"] = '5a46fc92d36e604f423286c04875437f'



cred = credentials.Certificate("PrivateKey.json")
firebase_admin.initialize_app(cred)



@app.route("/",methods =["GET","POST"] )
@app.route("/KayitOl",methods =["GET","POST"] )
def kayitOl() :
    form = YeniKayitFormu()
    return render_template ("KayitOl.html" ,baslik = "kayitOl", f =form )

@app.route("/Login",methods =["GET","POST"] )
def login() :
    form = LoginForm()
    return render_template ("GirisYap.html" ,baslik = "Login", f =form )

if __name__ == "__main__": 
    app.run(debug=True)