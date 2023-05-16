from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, send_file
from .models import User
from . import db, USERSDATA_PATH, ANALYSIS_DIR
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from HSEER import get_webcam, HSEER_model
import calendar
import pandas as pd
from datetime import datetime
import io
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


DEVICE = get_webcam.DEVICE
MODEL_PATH = 'HSEER\models\enet_b0_8_va_mtl.pt'
# MODEL_PATH = 'HSEER\models\enet_b2_8_best.pt'
auth = Blueprint('auth', __name__)
webcam = get_webcam.WebCam()
model = HSEER_model.HSEER(model_path=MODEL_PATH, device='cpu')
sns.set_theme()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                face_image = webcam.detect_face()
                emotion = model.predict_emotion(face_image)

                users_data = pd.read_csv(USERSDATA_PATH)
                listik = users_data[users_data['user_email'] == email].values[0]
                current_email, position, sex, age = listik[1:5]
                current_id = len(users_data) 
                now = datetime.now()
                current_date = now.strftime("%d/%m/%Y %H:%M:%S")
                weekday = calendar.day_name[datetime.strptime(current_date, "%d/%m/%Y %H:%M:%S").weekday()]
                is_weekend = True if weekday == 'Sunday' or weekday == 'Saturday' else False
                
                with open(USERSDATA_PATH, 'a+') as file:
                    data_to_write = f'{current_id},{current_email},{position},{sex},{age},{current_date},{weekday},{is_weekend},{emotion}\n'
                    file.write(data_to_write)

                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        feature = request.form.get('analyze_input')
        usersdata = pd.read_csv(USERSDATA_PATH)
        now = datetime.now()
        current_date = now.strftime("%d-%m-%Y")

        if feature == 'age':
            lambda_f = lambda age: 0 if age < 18 else (1 if 18 <= age < 40 else (2 if 40 <= age <= 90 else 3))
            usersdata['age_category'] = usersdata['age'].apply(lambda_f)

            age_category_dict = {0: 'teenagers', 1: 'young adults', 2: 'middle-aged_adults', 3: 'old_adults'}
            feature = 'age_category'

        figure = plt.figure(figsize=(16, 8))
        sns.countplot(data=usersdata, x=feature, hue='emotion', dodge=True)
        plt.legend(loc='upper right')
        if feature == 'age_category':
            plt.xticks([0,1,2,3],['teenagers', 'young_adults', 'middle_aged_adults', 'old_adults'])
        plt.savefig(ANALYSIS_DIR + f'{feature}_{current_date}_analysis.png')
        
        

        return redirect(url_for('views.home'))
    
    return render_template("analyze.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    email = current_user.email
    face_image = webcam.detect_face()
    emotion = model.predict_emotion(face_image)

    users_data = pd.read_csv(USERSDATA_PATH)
    listik = users_data[users_data['user_email'] == email].values[0]
    current_email, position, sex, age = listik[1:5]
    current_id = len(users_data) 
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y %H:%M:%S")
    weekday = calendar.day_name[datetime.strptime(current_date, "%d/%m/%Y %H:%M:%S").weekday()]
    is_weekend = True if weekday == 'Sunday' or weekday == 'Saturday' else False
                
    with open(USERSDATA_PATH, 'a+') as file:
        data_to_write = f'{current_id},{current_email},{position},{sex},{age},{current_date},{weekday},{is_weekend},{emotion}\n'
        file.write(data_to_write)
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        secondName = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        sex = request.form.get('sex')
        position = request.form.get('position')
        age = request.form.get('age')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(secondName) < 2:
            flash('Second name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        elif len(sex) == 0:
            flash('Sex must be filled.', category='error')
        elif len(position) == 0:
            flash('Position must be filled.', category='error')
        elif len(age) == 0:
            flash('Age must be filled.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, second_name=secondName, 
                password=generate_password_hash(password1, method='sha256'), sex=sex, position=position, age=age)
            
            db.session.add(new_user)
            db.session.commit()

            face_image = webcam.detect_face()
            emotion = model.predict_emotion(face_image)

            users_data = pd.read_csv(USERSDATA_PATH)
            current_id = len(users_data) 
            now = datetime.now()
            current_date = now.strftime("%d/%m/%Y %H:%M:%S")
            weekday = calendar.day_name[datetime.strptime(current_date, "%d/%m/%Y %H:%M:%S").weekday()]
            is_weekend = True if weekday == 'Sunday' or weekday == 'Saturday' else False

            with open(USERSDATA_PATH, 'a+') as file:
                data_to_write = f'{current_id},{email},{position},{sex},{age},{current_date},{weekday},{is_weekend},{emotion}\n'
                file.write(data_to_write)

            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)