from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    ziyaretciler = db.relationship('Ziyaretci', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ziyaretci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    aciklama = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ziyaretciler')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Bu e-posta zaten kayıtlı.", "danger")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Şifreler eşleşmiyor!", "danger")
            return redirect(url_for('register'))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Geçersiz e-posta veya şifre.", "danger")
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    toplam_ziyaretci = Ziyaretci.query.count()
    son_ziyaretciler = Ziyaretci.query.order_by(Ziyaretci.tarih.desc()).limit(5).all()
    return render_template('dashboard.html', toplam_ziyaretci=toplam_ziyaretci, son_ziyaretciler=son_ziyaretciler)


@app.route('/ziyaretci_ekleme', methods=['GET', 'POST'])
@login_required
def ziyaretci_ekleme():
    if request.method == 'POST':
        ad_soyad = request.form['ad_soyad']
        aciklama = request.form['aciklama']
        tarih = datetime.now()

        yeni_ziyaretci = Ziyaretci(
            ad_soyad=ad_soyad,
            aciklama=aciklama,
            tarih=tarih,
            user_id=current_user.id  # Burada current_user id'sini atıyoruz
        )
        db.session.add(yeni_ziyaretci)
        db.session.commit()

        flash("Ziyaretçi başarıyla eklendi.", "success")
        return redirect(url_for('ziyaretci_liste'))

    return render_template('ziyaretci_ekleme.html')


@app.route('/ziyaretci_liste/guncelle/<int:id>', methods=['GET', 'POST'])
@login_required
def ziyaretci_güncelleme(id):
    ziyaretci = Ziyaretci.query.get_or_404(id)

    if request.method == 'POST':
        ziyaretci.ad_soyad = request.form['ad_soyad']

        tarih_str = request.form['tarih']  # 'YYYY-MM-DD' formatında string gelir
        ziyaretci.tarih = datetime.strptime(tarih_str, '%Y-%m-%d')  # datetime objesine çevir

        ziyaretci.aciklama = request.form['aciklama']
        db.session.commit()
        flash('Ziyaretçi bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('ziyaretci_liste'))

    return render_template('ziyaretci_güncelleme.html', ziyaretci=ziyaretci)


@app.route('/ziyaretci_liste/sil/<int:id>', methods=['POST', 'GET'])
@login_required
def ziyaretci_sil(id):
    ziyaretci = Ziyaretci.query.get_or_404(id)
    try:
        db.session.delete(ziyaretci)
        db.session.commit()
        flash('Ziyaretçi başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Silme işlemi sırasında hata oluştu: {e}', 'danger')
    return redirect(url_for('ziyaretci_liste'))


@app.route('/ziyaretci_liste')
@login_required
def ziyaretci_liste():
    ziyaretciler = Ziyaretci.query.all()
    return render_template('ziyaretci_liste.html', ziyaretciler=ziyaretciler)


@app.route('/kullanicilar')
@login_required
def kullanicilar():
    users = User.query.all()
    return render_template('kullanicilar.html', users=users)


@app.route('/kullanici_ekle', methods=['POST'])
@login_required
def kullanici_ekle():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Bu e-posta zaten kayıtlı.", "danger")
    else:
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Kullanıcı başarıyla eklendi.", "success")

    return redirect(url_for('kullanicilar'))


@app.route('/kullanici_guncelle/<int:user_id>', methods=['GET', 'POST'])
@login_required
def kullanici_guncelle(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        if user.email != new_email:
            if User.query.filter_by(email=new_email).first():
                flash("Bu e-posta başka bir kullanıcıda kayıtlı.", "danger")
                return redirect(url_for('kullanici_guncelle', user_id=user_id))
            user.email = new_email

        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash("Kullanıcı güncellendi.", "success")
        return redirect(url_for('kullanicilar'))

    return render_template('kullanici_guncelle.html', user=user)


@app.route('/kullanici/sil/<int:user_id>', methods=['POST'])
@login_required
def kullanici_sil(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Kullanıcı başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Kullanıcı silinirken bir hata oluştu: {e}', 'danger')
    return redirect(url_for('kullanicilar'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Başarıyla çıkış yapıldı.", "success")
    return redirect(url_for('login'))
if name == "main":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
