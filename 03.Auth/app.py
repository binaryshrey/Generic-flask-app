#JWT : JSON Web Token (JWT) is an open standard  that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.
#JSON Web Token structure : Header, Payload, Signature

from flask import Flask,request
from flask_restful import Resource, Api
from flask_jwt import JWT,jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'binary'
api = Api(app)

jwt = JWT(app, authenticate, identity)    # /auth

items = []

class Item(Resource):

    @jwt_required()
    #authenticates the user with the JWT token creted from /auth route
    def get(self,name):
        item = next(filter(lambda x: x['name']  ==  name, items),None)
        return {'item'  :   item}, 200 if item else 400
    
    def post(self, name):
        if(next(filter(lambda x: x['name']  ==  name,items),None))  is not None:
            return (f'an item with name {name} already exists'), 400

        req_data = request.get_json()
        new_item = {
            'name'  :   name,
            'price' :   req_data['price']
        }
        items.append(new_item)
        return new_item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x:x["name"] != name,items))
        return {"message"   :   "Item deleted"}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x : x['name'] == name, items),None)
        if item is None:
            item = {
                'name'  :   name,
                'price' :   data['price']
            }
            items.append(item)
        else:
            item.update(data)
        return item



class ItemsList(Resource):
    def get(self):
        return ({'items' : items})



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemsList,'/items')
app.run(port=5000, debug=True)



