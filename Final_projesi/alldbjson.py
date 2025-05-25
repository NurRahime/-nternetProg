from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    ziyaretciler = db.relationship('Ziyaretci', back_populates='user', lazy=True)


class Ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    aciklama = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ziyaretciler')

def to_dict():
    with app.app_context():
        users = User.query.all()
        data = []

        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'ziyaretciler': []
            }

            for z in user.ziyaretciler:
                ziyaretciler_list = {
                    'id': z.id,
                    'ad_soyad': z.ad_soyad,
                    'tarih': z.tarih.strftime('%Y-%m-%d %H:%M:%S') if z.tarih else None,
                    'aciklama': z.aciklama,
                    'user_id': z.user_id
                }
                user_data['ziyaretciler'].append(ziyaretciler_list)

            data.append(user_data)

        with open('alldb.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Veriler JSON dosyasına yazıldı.")


if __name__ == '__main__':
    to_dict()