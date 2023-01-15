from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import os
import base64
import onetimepass



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    otp = db.Column(db.Boolean, nullable=False)
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo'.format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)