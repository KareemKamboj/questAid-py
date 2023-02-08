from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Deck:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.number_of_cards = data['number_of_cards']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod 
    def create(cls, data):
        query = "INSERT INTO flash_cards (name, number_of_cards, user_id) VALUES (%(name)s, %(number_of_cards)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM flash_cards JOIN users on flash_cards.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_decks = []
            for row in results:
                this_deck = cls(row)
                user_data = {
                    **row,
                    'id': row['user_id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_deck.person = this_user
                all_decks.append(this_deck)
            return all_decks
        return []

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM flash_cards JOIN users on users.id = flash_cards.user_id WHERE flash_cards.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        this_deck = cls(row)
        user_data = {
            **row,
            'id': row['user_id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        person = user_model.User(user_data)
        this_deck.person = person
        return this_deck

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM flash_cards WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE flash_cards SET name = %(name)s, number_of_cards = %(number_of_cards)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 1:
            flash("name required")
            is_valid = False
        if len(form_data['number_of_cards']) < 1:
            flash("number of cards required")
            is_valid = False
        return is_valid