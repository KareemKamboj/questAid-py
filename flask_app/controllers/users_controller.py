from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.decks_model import Deck

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass
    }
    id = User.create(data)
    session['user_id'] = id
    return redirect('/profile')


@app.route('/users/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid login info', 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid login info', 'log')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/profile')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/') 
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('profile.html', user=user)

@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')

@app.route('/flashcards')
def flash_cards():
    if 'user_id' not in session:
        return redirect('/')
    all_decks = Deck.get_all()
    user_data = {
        'id': session['user_id'],
        'email': session['email']
    }
    user = User.get_by_email(user_data)
    return render_template('flash_cards.html', user=user, all_decks=all_decks)