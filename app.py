from flask import Flask, render_template
from models import db, Hero, About, CreativeWriting, ContentWriting, Leadership, Advocacy, Project, Media, Volunteering, ContactInfo, Message, User
from flask import Flask, render_template, request, flash, redirect, url_for
#from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import os
app = Flask(__name__)
app.secret_key = "supersecretkey"  
# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "your_email@gmail.com"   # your email
app.config['MAIL_PASSWORD'] = "your_app_password"      # app password, not raw Gmail password
app.config['MAIL_DEFAULT_SENDER'] = ("Portfolio Website", "your_email@gmail.com")
#mail = Mail(app)

db.init_app(app)
import os

# Set upload folder (inside static/images)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
# Setup Login Manager
login_manager = LoginManager()
login_manager.login_view = "login"  # redirect to login if not authenticated
login_manager.init_app(app)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# Create tables & default data
with app.app_context():
    db.create_all()

    # Hero default
    if Hero.query.count() == 0:
        hero = Hero(
            name="Ijeoma Anastasia Ntada",
            intro="Meet Me. I am Ijeoma Anastasia Ntada. A layered person — creative writer, content marketer, advocate, and leader.",
            image="images/profile.jpg"
        )
        db.session.add(hero)

    # About default
    if About.query.count() == 0:
        about = About(
            bio="""I am a final-year Medical Laboratory Science student with a passion for 
            communication, creative writing, content marketing, and youth advocacy. 
            I wear many hats — storyteller, marketer, advocate, and leader — and 
            believe in using words and action to drive change.""",
            profile_image="images/profile.jpg"
        )
        db.session.add(about)

    # Creative Writing default
    if CreativeWriting.query.count() == 0:
        cw1 = CreativeWriting(
            title="Afrocritik Essay: The Power of African Storytelling",
            description="An essay published on Afrocritik exploring identity and narrative.",
            link="https://afrocritik.com/sample-essay",
            image="images/writing1.jpg"
        )
        cw2 = CreativeWriting(
            title="From Ije, With Love (Substack)",
            description="Personal newsletter on life, culture, and growth.",
            link="https://substack.com/@ijeoma",
            image="images/writing2.jpg"
        )
        db.session.add_all([cw1, cw2])

    # Content Marketing default
    if ContentWriting.query.count() == 0:
        cm1 = ContentWriting(
            title="Clever Campus Lead Campaign Project",
            description="Led marketing campaigns focused on student engagement and advocacy.",
            link="#",
            image="images/writing1.jpg"
        )
        cm2 = ContentWriting(
            title="Professional Content Writing Portfolio",
            description="Selected professional content writing samples.",
            link="#",
            image="images/writing2.jpg"
        )
        db.session.add_all([cm1, cm2])

    db.session.commit()

    # Leadership roles
    if Leadership.query.count() == 0:
        l1 = Leadership(
            role="Director of SDGs",
            organization="Junior Chamber International (JCI)",
            year="2023",
            description="Led sustainable development initiatives and community outreach."
        )
        l2 = Leadership(
            role="Press Secretary to the SDG President",
            organization="SDGs Office",
            year="2023–2024",
            description="Managed communications and media strategy for SDG President."
        )
        l3 = Leadership(
            role="Clever Campus Lead",
            organization="Clever Campus",
            year="2024",
            description="Advocated for student-focused marketing and campaigns."
        )
        db.session.add_all([l1, l2, l3])

    # Advocacy campaigns
    if Advocacy.query.count() == 0:
        a1 = Advocacy(
            title="Founder & Executive Director, Girls for Health and Literacy (GHL)",
            description="Founded GHL to empower girls through health and literacy programs.",
            image="images/advocacy1.jpg"
        )
        a2 = Advocacy(
            title="Cervical & Breast Cancer Awareness Campaigns",
            description="Organized awareness projects with measurable community impact.",
            image="images/advocacy2.jpg"
        )
        db.session.add_all([a1, a2])

    db.session.commit()


    # Projects defaults
    if Project.query.count() == 0:
        p1 = Project(
            title="Breast Cancer Awareness Project",
            description="Organized outreach programs to educate women on breast cancer prevention and early detection.",
            impact="Reached over 500 women with life-saving information.",
            image="images/project1.jpg"
        )
        p2 = Project(
            title="Cervical Cancer Awareness Project",
            description="Led a health campaign spreading awareness on cervical cancer.",
            impact="Distributed over 1,000 flyers and hosted 2 seminars.",
            image="images/project2.jpg"
        )
        p3 = Project(
            title="JCI International Day of the Girl Child",
            description="Coordinated a campaign celebrating and empowering girls.",
            impact="Partnered with NGOs and engaged 200+ students.",
            image="images/project3.jpg"
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

    # Media defaults
    if Media.query.count() == 0:
        m1 = Media(
            title="Conversations with Ije – Episode 1",
            description="Instagram Live series exploring youth leadership and storytelling.",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",  # replace with real link
            thumbnail="images/media1.jpg"
        )
        m2 = Media(
            title="Girls for Health and Literacy Campaign Video",
            description="Short documentary on the GHL campaign.",
            video_url="https://www.youtube.com/embed/9bZkp7q19f0",  # replace with real link
            thumbnail="images/media2.jpg"
        )
        db.session.add_all([m1, m2])
        db.session.commit()


    # Volunteering defaults
    if Volunteering.query.count() == 0:
        v1 = Volunteering(
            organization="Red Cross",
            role="Health Volunteer",
            year="2022",
            description="Assisted in community health drives and emergency relief programs.",
            image="images/volunteer1.jpg"
        )
        v2 = Volunteering(
            organization="World Literacy Foundation",
            role="Campaign Volunteer",
            year="2023",
            description="Supported global literacy campaigns by mobilizing youth in Nigeria.",
            image="images/volunteer2.jpg"
        )
        v3 = Volunteering(
            organization="JCI Community Projects",
            role="Event Volunteer",
            year="2023",
            description="Helped organize local SDG events with youth engagement.",
            image="images/volunteer3.jpg"
        )
        db.session.add_all([v1, v2, v3])
        db.session.commit()


# needed for flash messages

with app.app_context():
    db.create_all()

    # Contact defaults
    if ContactInfo.query.count() == 0:
        contact = ContactInfo(
            email="ijeoma@example.com",
            instagram="https://instagram.com/ijeoma",
            substack="https://substack.com/@ijeoma",
            linkedin="https://linkedin.com/in/ijeoma"
        )
        db.session.add(contact)
        db.session.commit()

# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    hero = Hero.query.first()
    contact_info = ContactInfo.query.first()

    if request.method == 'POST':
        user_name = request.form.get('name', '').strip()
        user_email = request.form.get('email', '').strip()
        user_message = request.form.get('message', '').strip()

        if not user_name or not user_email or not user_message:
            flash("Please fill in all fields.", "error")
        else:
            # Save the message to the database
            new_msg = Message(name=user_name, email=user_email, message=user_message)
            db.session.add(new_msg)
            db.session.commit()
            flash("Your message has been received! Thank you for reaching out to Ijeoma.", "success")

        return redirect(url_for('contact'))

    return render_template('contact.html', contact=contact_info,hero=hero)



with app.app_context():
    if User.query.count() == 0:
        admin = User(username="ijeoma")
        admin.set_password("ijeoma123")  # change later
        db.session.add(admin)
        db.session.commit()

# Routes
@app.route('/')
def home():
    hero = Hero.query.first()
    return render_template('home.html', hero=hero)

@app.route('/about')
def about():
    hero = Hero.query.first()
    about_data = About.query.first()
    return render_template('about.html', about=about_data,hero=hero)

@app.route('/writing')
def writing():
    hero = Hero.query.first()
    creative = CreativeWriting.query.all()
    content = ContentWriting.query.all()
    return render_template('writing.html', creative=creative, content=content, hero=hero)


@app.route('/leadership')
def leadership():
    hero = Hero.query.first()
    leadership_roles = Leadership.query.all()
    advocacy_items = Advocacy.query.all()
    return render_template('leadership.html', leadership_roles=leadership_roles, advocacy_items=advocacy_items, hero=hero)


@app.route('/media')
def media():
    hero = Hero.query.first()
    media_items = Media.query.all()
    return render_template('media.html', media_items=media_items,hero=hero)


@app.route('/projects')
def projects():
    hero = Hero.query.first()
    projects = Project.query.all()
    return render_template('projects.html', projects=projects,hero=hero)


@app.route('/volunteering')
def volunteering():
    hero = Hero.query.first()
    volunteering_items = Volunteering.query.all()
    return render_template('volunteering.html', volunteering_items=volunteering_items,hero=hero)

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")


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

from werkzeug.utils import secure_filename
import os

# --- Hero Admin Route ---
@app.route('/admin/hero', methods=['GET', 'POST'])
@login_required
def admin_hero():
    hero = Hero.query.first()

    if request.method == 'POST':
        hero.name = request.form.get('name', hero.name)
        hero.intro = request.form.get('intro', hero.intro)

        # Handle profile image upload
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join('static/images', filename)
                image.save(image_path)
                hero.image = f'images/{filename}'  # stored relative to /static

        db.session.commit()
        flash("Hero section updated successfully!", "success")
        return redirect(url_for('admin_hero'))

    return render_template('admin/edit_hero.html', hero=hero)

@app.route('/admin/about', methods=['GET', 'POST'])
@login_required
def admin_about():
    about = About.query.first()

    if request.method == 'POST':
        about.bio = request.form.get('bio', about.bio)

        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                about.profile_image = f'images/{filename}'  # relative to /static

        db.session.commit()
        flash("About section updated successfully!", "success")
        return redirect(url_for('admin_about'))

    return render_template('admin/edit_about.html', about=about)


# List all media items
@app.route('/admin/media')
@login_required
def admin_media():
    media_items = Media.query.all()
    return render_template("admin/manage_media.html", media=media_items)

# Add new media
@app.route('/admin/media/add', methods=['GET', 'POST'])
@login_required
def add_media():
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        description = request.form.get('description')

        thumbnail_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)

                # ensure upload folder exists
                upload_folder = os.path.join(app.static_folder, 'images')
                os.makedirs(upload_folder, exist_ok=True)

                save_path = os.path.join(upload_folder, filename)
                image.save(save_path)

                # ✅ save relative path to static
                thumbnail_path = f'images/{filename}'

        # ✅ use thumbnail instead of image
        new_media = Media(
            title=title,
            video_url=video_url,
            description=description,
            thumbnail=thumbnail_path
        )

        db.session.add(new_media)
        db.session.commit()
        flash("Media item added successfully!", "success")
        return redirect(url_for('admin_media'))

    return render_template("admin/add_media.html")


# Edit media
@app.route('/admin/media/edit/<int:media_id>', methods=['GET', 'POST'])
@login_required
def edit_media(media_id):
    item = Media.query.get_or_404(media_id)

    if request.method == 'POST':
        item.title = request.form.get('title', item.title)
        item.video_url = request.form.get('video_url', item.video_url)
        item.description = request.form.get('description', item.description)

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)

                # ensure upload folder exists
                upload_folder = os.path.join(app.static_folder, 'images')
                os.makedirs(upload_folder, exist_ok=True)

                save_path = os.path.join(upload_folder, filename)
                image.save(save_path)

                # ✅ update thumbnail path in DB
                item.thumbnail = f'images/{filename}'

        db.session.commit()
        flash("Media item updated!", "success")
        return redirect(url_for('admin_media'))

    return render_template("admin/edit_media.html", item=item)


# Delete media
@app.route('/admin/media/delete/<int:media_id>', methods=['POST'])
@login_required
def delete_media(media_id):
    item = Media.query.get_or_404(media_id)
    db.session.delete(item)
    db.session.commit()
    flash("Media item deleted!", "success")
    return redirect(url_for('admin_media'))

# List all projects
@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.all()
    return render_template("admin/manage_projects.html", projects=projects)

# Add project
@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        impact = request.form.get('impact')

        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                image_path = f'images/{filename}'

        new_project = Project(title=title, description=description, impact=impact, image=image_path)
        db.session.add(new_project)
        db.session.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for('admin_projects'))

    return render_template("admin/add_project.html")

# Edit project
@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title', project.title)
        project.description = request.form.get('description', project.description)
        project.impact = request.form.get('impact', project.impact)

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                project.image = f'images/{filename}'

        db.session.commit()
        flash("Project updated!", "success")
        return redirect(url_for('admin_projects'))

    return render_template("admin/edit_project.html", project=project)

# Delete project
@app.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted!", "success")
    return redirect(url_for('admin_projects'))

# Manage Creative Writing
@app.route('/admin/creative-writing')
@login_required
def admin_creative_writing():
    writings = CreativeWriting.query.all()
    return render_template("admin/manage_creative_writing.html", writings=writings)

@app.route('/admin/creative-writing/add', methods=['GET', 'POST'])
@login_required
def add_creative_writing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                image_path = f'images/{filename}'

        new_item = CreativeWriting(title=title, description=description, link=link, image=image_path)
        db.session.add(new_item)
        db.session.commit()
        flash("Creative Writing added!", "success")
        return redirect(url_for('admin_creative_writing'))

    return render_template("admin/add_creative_writing.html")

@app.route('/admin/creative-writing/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_creative_writing(item_id):
    item = CreativeWriting.query.get_or_404(item_id)

    if request.method == 'POST':
        item.title = request.form.get('title', item.title)
        item.description = request.form.get('description', item.description)
        item.link = request.form.get('link', item.link)

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                item.image = f'images/{filename}'

        db.session.commit()
        flash("Creative Writing updated!", "success")
        return redirect(url_for('admin_creative_writing'))

    return render_template("admin/edit_creative_writing.html", item=item)

@app.route('/admin/creative-writing/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_creative_writing(item_id):
    item = CreativeWriting.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Creative Writing deleted!", "success")
    return redirect(url_for('admin_creative_writing'))
# Manage Content Writing
@app.route('/admin/content-writing')
@login_required
def admin_content_writing():
    writings = ContentWriting.query.all()
    return render_template("admin/manage_content_writing.html", writings=writings)

@app.route('/admin/content-writing/add', methods=['GET', 'POST'])
@login_required
def add_content_writing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                image_path = f'images/{filename}'

        new_item = ContentWriting(title=title, description=description, link=link, image=image_path)
        db.session.add(new_item)
        db.session.commit()
        flash("Content Writing added!", "success")
        return redirect(url_for('admin_content_writing'))

    return render_template("admin/add_content_writing.html")

@app.route('/admin/content-writing/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_content_writing(item_id):
    item = ContentWriting.query.get_or_404(item_id)

    if request.method == 'POST':
        item.title = request.form.get('title', item.title)
        item.description = request.form.get('description', item.description)
        item.link = request.form.get('link', item.link)

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                item.image = f'images/{filename}'

        db.session.commit()
        flash("Content Writing updated!", "success")
        return redirect(url_for('admin_content_writing'))

    return render_template("admin/edit_content_writing.html", item=item)

@app.route('/admin/content-writing/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_content_writing(item_id):
    item = ContentWriting.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Content Writing deleted!", "success")
    return redirect(url_for('admin_content_writing'))

# ---------------- VOLUNTEERING ADMIN ---------------- #

@app.route('/admin/volunteering')
@login_required
def admin_volunteering():
    volunteering_items = Volunteering.query.all()
    return render_template("admin/manage_volunteering.html", volunteering=volunteering_items)


@app.route('/admin/volunteering/add', methods=['GET', 'POST'])
@login_required
def add_volunteering():
    if request.method == 'POST':
        organization = request.form.get('organization')
        role = request.form.get('role')
        year = request.form.get('year')
        description = request.form.get('description')

        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                image_path = f'images/{filename}'

        new_volunteer = Volunteering(
            organization=organization,
            role=role,
            year=year,
            description=description,
            image=image_path
        )
        db.session.add(new_volunteer)
        db.session.commit()
        flash("Volunteering record added successfully!", "success")
        return redirect(url_for('admin_volunteering'))

    return render_template("admin/add_volunteering.html")


@app.route('/admin/volunteering/edit/<int:volunteer_id>', methods=['GET', 'POST'])
@login_required
def edit_volunteering(volunteer_id):
    volunteer = Volunteering.query.get_or_404(volunteer_id)

    if request.method == 'POST':
        volunteer.organization = request.form.get('organization', volunteer.organization)
        volunteer.role = request.form.get('role', volunteer.role)
        volunteer.year = request.form.get('year', volunteer.year)
        volunteer.description = request.form.get('description', volunteer.description)

        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                volunteer.image = f'images/{filename}'

        db.session.commit()
        flash("Volunteering record updated successfully!", "success")
        return redirect(url_for('admin_volunteering'))

    return render_template("admin/edit_volunteering.html", volunteer=volunteer)


@app.route('/admin/volunteering/delete/<int:volunteer_id>', methods=['POST'])
@login_required
def delete_volunteering(volunteer_id):
    volunteer = Volunteering.query.get_or_404(volunteer_id)
    db.session.delete(volunteer)
    db.session.commit()
    flash("Volunteering record deleted successfully!", "success")
    return redirect(url_for('admin_volunteering'))

# ---------------- LEADERSHIP ADMIN ---------------- #

@app.route('/admin/leadership')
@login_required
def admin_leadership():
    leadership_items = Leadership.query.all()
    return render_template("admin/manage_leadership.html", leadership=leadership_items)


@app.route('/admin/leadership/add', methods=['GET', 'POST'])
@login_required
def add_leadership():
    if request.method == 'POST':
        role = request.form.get('role')
        organization = request.form.get('organization')
        year = request.form.get('year')
        description = request.form.get('description')

        new_leadership = Leadership(
            role=role,
            organization=organization,
            year=year,
            description=description
        )
        db.session.add(new_leadership)
        db.session.commit()
        flash("Leadership record added successfully!", "success")
        return redirect(url_for('admin_leadership'))

    return render_template("admin/add_leadership.html")


@app.route('/admin/leadership/edit/<int:leadership_id>', methods=['GET', 'POST'])
@login_required
def edit_leadership(leadership_id):
    item = Leadership.query.get_or_404(leadership_id)

    if request.method == 'POST':
        item.role = request.form.get('role', item.role)
        item.organization = request.form.get('organization', item.organization)
        item.year = request.form.get('year', item.year)
        item.description = request.form.get('description', item.description)

        db.session.commit()
        flash("Leadership record updated successfully!", "success")
        return redirect(url_for('admin_leadership'))

    return render_template("admin/edit_leadership.html", item=item)


@app.route('/admin/leadership/delete/<int:leadership_id>', methods=['POST'])
@login_required
def delete_leadership(leadership_id):
    item = Leadership.query.get_or_404(leadership_id)
    db.session.delete(item)
    db.session.commit()
    flash("Leadership record deleted successfully!", "success")
    return redirect(url_for('admin_leadership'))

@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template('admin/manage_messages.html', messages=messages)


@app.route('/admin/messages/delete/<int:msg_id>', methods=['POST'])
@login_required
def delete_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect(url_for('admin_messages'))


if __name__ == '__main__':
    app.run(debug=True)


