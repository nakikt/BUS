
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp, qrcode
from io import BytesIO
import base64
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():

    new_user = User(username="a", password=generate_password_hash("12345", method='sha256'), otp=False)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)

    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]
        otp_verification = request.json["otp_verification"]

        user = User.query.filter_by(username=username).first()
        if user:
            if otp_verification:
                if user.otp:
                    response = "That's not the first time you're logging"
                    return (jsonify(response), 403)
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    response = 'Gonna show you QR code'
                    return (jsonify(response), 202)
                else:
                    response = 'Wrong password'
                    return (jsonify(response), 404)
            else:
                otp = request.json["otp"]
                print(otp)
                if  user.verify_totp(otp): 
                    login_user(user, remember=True)
                    response = 'Login successful'
                    return (jsonify(response), 201)
                else:
                    response = 'Wrong token'
                    return (jsonify(response), 402)
        else:
            response = 'Wrong credentials'
            return (jsonify(response), 401)

    return render_template("login.html", user=current_user)




@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route('/twofactor')
@login_required
def two_factor_setup():

    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two-factor-setup.html', user = current_user), 200

@auth.route('/qr')
@login_required
def qr():

    user = current_user
    # render qrcode for FreeTOTP
    url = qrcode.make(user.get_totp_uri())
    qrcode.make(user.get_totp_uri()).save("website/code.png")
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200

@auth.route('/getqr')
@login_required
def getqr():
    user = current_user
    url = qrcode.make(user.get_totp_uri())
    qrcode.make(user.get_totp_uri()).save("website/code.png")

    prefix = f'data:image/png;base64,'
    with open('website/code.png', 'rb') as f:
        img = f.read()
    response = prefix + base64.b64encode(img).decode('utf-8')

    return (jsonify(response), 200)

@auth.route("/check" ,methods=['GET', 'POST'])
def check_otp():
    if request.method == 'POST':
        otp = request.form.get("otp")


