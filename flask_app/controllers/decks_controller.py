from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.decks_model import Deck
from flask_app.models.cards_model import Card

@app.route("/decks/new")
def new_deck_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_deck.html')

@app.route("/decks/create", methods=['POST'])
def process_deck():
    if 'user_id' not in session:
        return redirect('/')
    if not Deck.validator(request.form):
        return redirect('/decks/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    id = Deck.create(data)
    # return redirect(f'/decks/{id}')
    return redirect(f'/cards/new/{id}')

@app.route("/decks/<int:id>")
def show_deck(id):
    cards = Card.get_all_in_deck({'deck_id':id})
    deck = Deck.get_by_id({'id':id})
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template("one_deck.html", user=user, cards=cards, deck=deck)

@app.route("/decks/<int:id>/delete")
def del_deck(id):
    if 'user_id' not in session:
        return redirect('/')
    deck = Deck.get_by_id({'id':id})
    if not int(session['user_id']) == deck.user_id:
            flash("You cannot delete")
            return redirect('/flashcards')
    deck.delete({'id':id})
    return redirect('/flashcards')

@app.route("/decks/<int:id>/edit")
def edit_deck(id):
    if 'user_id' not in session:
        return redirect('/')
    deck = Deck.get_by_id({'id':id})
    if not int(session['user_id']) == deck.user_id:
        flash("You cannot edit")
        return redirect('/flashcards')
    deck = Deck.get_by_id({'id':id})
    return render_template("edit_flashcards.html", deck=deck)

@app.route("/decks/<int:id>/update", methods=['POST'])
def update_deck(id):
    if 'user_id' not in session:
        return redirect('/')
    deck = Deck.get_by_id({'id':id})
    if not int(session['user_id']) == deck.user_id:
        flash("You cannot update")
        return redirect('/flashcards')
    if not Deck.validator(request.form):
        return redirect(f'/decks/{id}/edit')
    data = {
        **request.form,
        'id':id
    }
    Deck.update(data)
    return redirect("/flashcards")