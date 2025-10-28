from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from models import db, Hero, About, CreativeWriting, ContentWriting, Leadership, Advocacy, Project, Media, Volunteering, ContactInfo, Message, User
import cloudinary
import cloudinary.uploader
import os

# ----------------- APP CONFIG -----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- DATABASE CONFIG ----------
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_mGgT2XhON4Al@ep-red-block-a4ds0axu-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ---------- CLOUDINARY CONFIG ----------
cloudinary.config(
    cloud_name="dnitmwnru",     # replace with your actual Cloudinary cloud name
    api_key="625647693556616",           # replace with your API key
    api_secret="aWXD-UlPvpJd6knZ7L0LCpXTM6U",     # replace with your API secret
    secure=True
)

# ---------- INITIALIZE EXTENSIONS ----------
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- CLOUDINARY UPLOAD HELPER ----------
def upload_to_cloudinary(file):
    """Upload image or video to Cloudinary and return the public URL."""
    if file and file.filename != '':
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type="auto",  # auto-detect image or video
            folder="portfolio_uploads"
        )
        return upload_result.get("secure_url")
    return None

# ----------------- ROUTES -----------------

@app.route('/')
def home():
    hero = Hero.query.first()
    return render_template('home.html', hero=hero)

@app.route('/about')
def about():
    hero = Hero.query.first()
    about_data = About.query.first()
    return render_template('about.html', about=about_data, hero=hero)

# ---------- ADMIN HERO ----------
@app.route('/admin/hero', methods=['GET', 'POST'])
@login_required
def admin_hero():
    hero = Hero.query.first()
    if request.method == 'POST':
        hero.name = request.form.get('name', hero.name)
        hero.intro = request.form.get('intro', hero.intro)

        image = request.files.get('image')
        if image:
            hero.image = upload_to_cloudinary(image)

        db.session.commit()
        flash("Hero section updated successfully!", "success")
        return redirect(url_for('admin_hero'))

    return render_template('admin/edit_hero.html', hero=hero)

# ---------- ADMIN ABOUT ----------
@app.route('/admin/about', methods=['GET', 'POST'])
@login_required
def admin_about():
    about = About.query.first()
    if request.method == 'POST':
        about.bio = request.form.get('bio', about.bio)

        image = request.files.get('image')
        if image:
            about.profile_image = upload_to_cloudinary(image)

        db.session.commit()
        flash("About section updated successfully!", "success")
        return redirect(url_for('admin_about'))

    return render_template('admin/edit_about.html', about=about)

# ---------- ADMIN CREATIVE WRITING ----------
@app.route('/admin/creative-writing/add', methods=['GET', 'POST'])
@login_required
def add_creative_writing():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_entry = CreativeWriting(title=title, content=content, image=image_url)
        db.session.add(new_entry)
        db.session.commit()
        flash("Creative Writing entry added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_creative_writing.html")

# ---------- ADMIN CONTENT WRITING ----------
@app.route('/admin/content-writing/add', methods=['GET', 'POST'])
@login_required
def add_content_writing():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_entry = ContentWriting(title=title, content=content, image=image_url)
        db.session.add(new_entry)
        db.session.commit()
        flash("Content Writing entry added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_content_writing.html")

# ---------- ADMIN LEADERSHIP ----------
@app.route('/admin/leadership/add', methods=['GET', 'POST'])
@login_required
def add_leadership():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_entry = Leadership(title=title, description=description, image=image_url)
        db.session.add(new_entry)
        db.session.commit()
        flash("Leadership record added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_leadership.html")

# ---------- ADMIN ADVOCACY ----------
@app.route('/admin/advocacy/add', methods=['GET', 'POST'])
@login_required
def add_advocacy():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_entry = Advocacy(title=title, description=description, image=image_url)
        db.session.add(new_entry)
        db.session.commit()
        flash("Advocacy record added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_advocacy.html")

# ---------- ADMIN PROJECT ----------
@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        impact = request.form.get('impact')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_project = Project(title=title, description=description, impact=impact, image=image_url)
        db.session.add(new_project)
        db.session.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_project.html")

# ---------- ADMIN MEDIA ----------
@app.route('/admin/media/add', methods=['GET', 'POST'])
@login_required
def add_media():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_file = request.files.get('video')
        image_file = request.files.get('thumbnail')

        video_url = upload_to_cloudinary(video_file) if video_file else None
        image_url = upload_to_cloudinary(image_file) if image_file else None

        new_media = Media(title=title, description=description, video_url=video_url, thumbnail=image_url)
        db.session.add(new_media)
        db.session.commit()
        flash("Media added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_media.html")

# ---------- ADMIN VOLUNTEERING ----------
@app.route('/admin/volunteering/add', methods=['GET', 'POST'])
@login_required
def add_volunteering():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files.get('image')

        image_url = upload_to_cloudinary(image) if image else None

        new_entry = Volunteering(title=title, description=description, image=image_url)
        db.session.add(new_entry)
        db.session.commit()
        flash("Volunteering record added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/add_volunteering.html")

# ---------- CONTACT ----------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    hero = Hero.query.first()
    contact_info = ContactInfo.query.first()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
        else:
            new_msg = Message(name=name, email=email, message=message)
            db.session.add(new_msg)
            db.session.commit()
            flash("Your message has been received!", "success")

        return redirect(url_for('contact'))

    return render_template('contact.html', contact=contact_info, hero=hero)

# ---------- LOGIN / LOGOUT ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
