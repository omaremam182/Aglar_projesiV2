from queue import Full
from flask import Flask, flash , render_template,redirect, session, url_for
from Forms import *
# from firebase_admin import db
from firebase_config22 import fire,db
from datetime import datetime, timedelta

app = Flask (__name__)
app.config["SECRET_KEY"] = '5a46fc92d36e604f423286c04875437f' 
dogrulama = fire.auth()

# Oturum zaman aşımı süresi (saniye ile)
OTURUM_TIME = 1800  # 30 dakika

def check_session_timeout():
    if 'last_activity' in session:
        last_activity = session.get('last_activity')
        
        # last_activity bir string değilse oturum temizlensin
        if not isinstance(last_activity, str):
            session.clear()
            flash("Oturum bilgileriniz geçersiz. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for('login'))
        
        try:
            # Son aktiviteyi datetime formatına çevir
            last_request = datetime.fromisoformat(last_activity)
        except ValueError:
            session.clear()
            flash("Oturum bilgileriniz geçersiz. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for('login'))
        
        current_time = datetime.utcnow()
        time_difference = current_time - last_request
        if time_difference > timedelta(seconds=OTURUM_TIME):
            session.clear()
            flash("Oturum süreniz doldu. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for('login'))

    # Son aktiviteyi güncelle
    session['last_activity'] = datetime.utcnow().isoformat()


@app.route("/", methods=["GET", "POST"])
@app.route("/KayitOl", methods=["GET", "POST"])
def kayitOl():
    form = YeniKayitFormu()

    if form.validate_on_submit():
        email = form.Eposta.data
        sifre = form.sifre.data
        telefon = form.telefonNo.data
        kullaniciAdi = form.kullaniciAdi.data


        try:
            uye = dogrulama.create_user_with_email_and_password(email, sifre)
            # dogrulama.send_email_verification(uye['idToken'])
            uye_id = uye['localId'] 
            
            user_data = {
                "telefonNo": telefon,
                "kullaniciAdi": kullaniciAdi,
                "email": email 
            }
            db.collection("users").document(uye_id).set(user_data) 
            flash("Kayıt başarılı! ", "success")
            return redirect("/home")  
        
        except Exception as e:
            flash("Bu e-posta adresi zaten kullanımda. Lütfen başka bir e-posta girin"," error")
    
    return render_template("KayitOl.html", baslik="Kayıt Ol", f=form)

@app.route("/Login",methods =["GET","POST"] )
def login():
    form2 = LoginForm()

    if form2.validate_on_submit():
        email = form2.Eposta.data
        sifre = form2.sifre.data

        try:
            user = dogrulama.sign_in_with_email_and_password(email, sifre)
            if user:
                print(f"Giriş başarılı. Kullanıcı ID: {user['localId']}") # terminalde yazdırılacak

                session['user_id'] = user['localId']
                session['email'] = email
                session['last_activity'] = datetime.now()  
                flash("Giriş başarılı.", "success")
                return redirect("/home")  
            else:
                flash("Giriş bilgileri yanlış. Lütfen tekrar deneyin.", "error")

        except Exception as e:
            flash("Giriş yaparken bir hata oluştu: " + str(e), "error")

    return render_template("GirisYap.html", baslik="Login", f=form2)

@app.route("/sifremiUnuttum", methods=["GET", "POST"])
def sifremiunuttum():
    form3 = SifreSifirlama()
    if form3.validate_on_submit():
        email = form3.eposta.data
        try:
            dogrulama.send_password_reset_email(email)
            flash("E-posta adresinize şifre sıfırlama bağlantısı gönderildi.", "success")
            return redirect("/Login")
        except Exception as e:
            flash("Bir hata oluştu: " + str(e), "error")
    return render_template("sifremiUnuttum.html", baslik="Forgot password", f=form3)

@app.route("/home",methods=["GET","POST"])
def anaSayfa():
    check_session_timeout()
    return render_template("home.html")

if __name__ == "__main__": 
    app.run(debug=True)
