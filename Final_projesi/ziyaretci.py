from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    aciklama = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def export_ziyaretciler_to_json():
    with app.app_context():
        ziyaretciler = Ziyaretci.query.all()
        data = []
        for z in ziyaretciler:
            data.append({
                'id': z.id,
                'ad_soyad': z.ad_soyad,
                'tarih': z.tarih.strftime('%Y-%m-%d %H:%M:%S') if z.tarih else None,
                'aciklama': z.aciklama,
                'user_id': z.user_id
            })

        with open('ziyaretciler.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Ziyaretçiler başarıyla ziyaretciler.json dosyasına kaydedildi!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        export_ziyaretciler_to_json()
