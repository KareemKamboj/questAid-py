from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model, decks_model

class Card:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.front = data['front']
        self.back = data['back']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod 
    def create(cls, data):
        query = "INSERT INTO cards (front, back, user_id) VALUES (%(front)s,  %(back)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cards JOIN flash_cards on cards.user_id = flash_cards.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_cards = []
            for row in results:
                this_card = cls(row)
                user_data = {
                    **row,
                    'id': row['user_id'],
                    'created_at': row['flash_cards.created_at'],
                    'updated_at': row['flash_cards.updated_at']
                }
                this_user = user_model.User(user_data)
                this_card.person = this_user
                all_cards.append(this_card)
            return all_cards
        return []

    @classmethod
    def get_all_in_deck(cls, data):
        query = "SELECT * FROM cards WHERE user_id = %(deck_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            all_cards = []
            for row in results:
                this_card = cls(row)
                all_cards.append(this_card)
            return all_cards
        return []

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM cards JOIN flash_cards on flash_cards.id = cards.user_id WHERE cards.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        this_card = cls(row)
        user_data = {
            **row,
            'id': row['user_id'],
            'created_at': row['flash_cards.created_at'],
            'updated_at': row['flash_cards.updated_at']
        }
        # person = user_model.User(user_data)
        # this_card.person = person
        return this_card

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cards WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE cards SET front = %(front)s, back = %(back)s  WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['front']) < 1:
            flash("front required")
            is_valid = False
        if len(form_data['back']) < 1:
            flash("back required")
            is_valid = False
        return is_valid