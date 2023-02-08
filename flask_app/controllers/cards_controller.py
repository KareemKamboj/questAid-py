from flask_app import app
from flask import render_template, redirect, request, flash, session, jsonify
from flask_app.models.user_model import User
from flask_app.models.decks_model import Deck
from flask_app.models.cards_model import Card

@app.route("/cards/new/<int:deck_id>")
def new_card_form(deck_id):
    if 'user_id' not in session:
        return redirect('/')
    deck = Deck.get_by_id({'id':deck_id})
    return render_template('create_cards.html', deck=deck)

@app.route("/cards/create", methods=['POST'])
def process_card():
    if 'user_id' not in session:
        return redirect('/')
    if not Card.validator(request.form):
        return redirect('/cards/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    id = Card.create(data)
    return redirect(f'/cards/{id}')

@app.route("/api/cards/create", methods=['POST'])
def api_process_card():
    if 'user_id' not in session:
        return redirect('/')
    # if not Card.validator(request.form):
    #     return redirect('/cards/new')
    data = {
        **request.form
    }
    print(request.form)
    id = Card.create(data)
    response = {
        'id': id
    }
    return jsonify(response)

@app.route("/cards/<int:id>")
def show_cards(id):
    cards = Card.get_all_in_deck({'deck_id':id})
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template("one_deck.html", user=user, cards=cards)

@app.route("/cards/<int:id>/delete")
def del_card(id):
    if 'user_id' not in session:
        return redirect('/')
    card = Card.get_by_id({'id':id})
    if not int(session['user_id']) == card.user_id:
            flash("You cannot delete")
            return redirect('/flashcards')
    card.delete({'id':id})
    return redirect('/flashcards')

@app.route("/decks/<int:id>/edit")
def edit_card(id):
    if 'user_id' not in session:
        return redirect('/')
    card = Card.get_by_id({'id':id})
    if not int(session['user_id']) == card.user_id:
        flash("You cannot edit")
        return redirect('/flashcards')
    card = Card.get_by_id({'id':id})
    return render_template("edit_flashcards.html", card=card)

@app.route("/decks/<int:id>/update", methods=['POST'])
def update_card(id):
    if 'user_id' not in session:
        return redirect('/')
    card = Card.get_by_id({'id':id})
    if not int(session['user_id']) == card.user_id:
        flash("You cannot update")
        return redirect('/flashcards')
    if not Card.validator(request.form):
        return redirect(f'/cards/{id}/edit')
    data = {
        **request.form,
        'id':id
    }
    Card.update(data)
    return redirect("/flashcards")