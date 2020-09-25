from flask import Flask,request
from flask_restful import Resource, Api
#Resource : Any information that can be named can be a resource, every resource has to be a class 

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self,name):
        # for item in items:
        #     if(item['name'] == name):
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



class ItemsList(Resource):
    def get(self):
        return ({'items' : items})



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemsList,'/items')
app.run(port=5000, debug=True)



