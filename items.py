import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    # parser je sedaj del razreda, ne metode, da nimamo duplicirane kode
    parser = reqparse.RequestParser()
    parser.add_argument('price',    # ce ostalih argumentov ne navedemo, ne bodo sprejeti!!!
        type=float,
        required=True,
        help="To polje ne more biti prazno"
    )

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query,(name,))

        row = result.fetchone()
        connection.close()
        if row:
            return {'item':{'name':row[0],'price':row[1]}}
        return None


    @jwt_required()
    def get(self, name):  #name of the item
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def insert_item(cls, item): # v item imamo sedaj vrednosti!!!
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        result = cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()
        
    
    def post(self, name):  ## moramo imeti enako strukturo
        # error first approch
        item = Item.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' already exists.".format(name)},400

        data = Item.parser.parse_args()
        item = {'name': name, 'price':data['price']}
        self.insert_item(item)
        
        return item, 201 # Created OK!  202 is accepted when delaying creation
    
    def delete(self,name):
        item = Item.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name = ?"
            result = cursor.execute(query,(name,))
            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        return {'message': 'Item does not exists'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name) # trenutni item
        updated_item = {'name': name, 'price':data['price']} #nova cena za item
        if item is None:
            try:
                self.insert_item(updated_item)
            except:
                return {"message":"Insert into items failed"}, 500 #internal server error
        else:
            try:
                self.update_item(updated_item)
            except:
                return {"message":"update into items failed"}, 500 #internal server error
        return updated_item

    @classmethod
    def update_item(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        result = cursor.execute(query,(item['price'],item['name']))
        connection.commit()
        connection.close()
        return {'message': 'Item Updated'}
    

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        seznam =[]
        for row in result:
            seznam.append(row)

        connection.commit()
        connection.close()
        return seznam, 200