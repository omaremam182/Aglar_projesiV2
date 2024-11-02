from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import *
from flask import Flask 
app = Flask (__name__)
if __name__== "__main__":
    app.run(debug=True)

# def sifre_dogrulama(form, field):
#     sifre = field.data    
#     if len(sifre) < 8 or len(sifre) > 32:
#         raise ValidationError("Şifre en az 8, en fazla 32 karakter olmalıdır.")
#     if not any(karakter.islower() for karakter in sifre):
#         raise ValidationError("Şifre en az bir küçük harf içermelidir.")
#     if not any(karakter.isupper() for karakter in sifre):
#         raise ValidationError("Şifre en az bir büyük harf içermelidir.")
#     if not any(karakter.isdigit() for karakter in sifre):
#         raise ValidationError("Şifre en az bir rakam içermelidir.")


class YeniKayitFormu(FlaskForm) :
    kullaniciAdi = StringField("kullanıcı Adı ", validators=[DataRequired("bu alanı doldurmak zorunlu"),Length(min=2,max=25)])
    telefonNo =  StringField("Telefon Numarası ", validators=[DataRequired("Lütfen telefon numaranızı başında sıfır olmadan yazınız"),
        Length(min=10, max=10),Regexp(r'^\d*$')])
    
    # Eposta = StringField("email ", validators=[DataRequired("bu alanı doldurmak zorunlu"),Email()])

    sifre = PasswordField("Şifre ", validators=[DataRequired("Şifre 8 ile 32 karakter arasında olmalıdır"),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
        message="Şifre en az bir büyük harf, bir küçük harf ve bir rakam içermelidir"),
        Length(min=8, max=32)])
    # sifre = PasswordField("Şifre ", validators=[DataRequired("Şifre 8 ile 32 karakter arasında olmalıdır"),validate_password])    
    
    sifreTekrar = PasswordField("Şifre doğrulama ", validators=[DataRequired("bu alanı doldurmak zorunlu"),EqualTo(sifre)])
    buton = SubmitField("kayıt ol")
    
    
class LoginForm(FlaskForm) :
    telefonNo =  StringField("Telefon Numarası ", validators=[DataRequired("Lütfen telefon numaranızı başında sıfır olmadan yazınız"),
        Length(min=10, max=10),
        Regexp(r'^\d*$')])
    rememberMe = BooleanField("beni hatırla ")
    buton = SubmitField("kayıt ol")
    sifre = PasswordField("Şifre ", validators=[DataRequired("bu alanı doldurmak zorunlu")])

