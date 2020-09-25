from flask import Flask,jsonify,request
# class names     - Capital letter
# library names   - small letter


app = Flask(__name__)
#__name__ gives a uniques name to a file
# GET / HTTP/1.1
# (verb) (path)

# An API is an application programming interface. It is a set of rules that allow programs to share resources to each other. 
# The term REST stands for REpresentational State Transfer. It is an architectural style that defines a set of rules in order to create Web Services. In a client-server communication, REST suggests to create an object of the data requested by the client and send the values of the object in response to the user.
# Principles of REST API - Stateless,Uniform Interface, Cacheable, client-server architecture
# Methods of REST API - POST,GET,PUT,DELETE

stores = [
    {
        "name"  : "Blr-Store",
        "items" : [{
            "name"  :   "Chair",
            "price" :   100.00
        }]
    }
]

@app.route('/')
def home():
    return "Hello-World-Store!"

#GET - /stores :to get all stores list
@app.route('/stores')
def get_all_stores():
    return (jsonify({"stores"   :   stores}))

# POST - /store :to create a store
# add Content-type : application/json in Postman
@app.route('/store', methods=["POST"])
def create_store():
    req_data = request.get_json()
    new_store = {
        "name"  :   req_data["name"],
        "items" :   []
    }
    stores.append(new_store)
    return(jsonify(new_store))

# GET - /store/<string:name> :get store based on name
@app.route('/store/<string:name>')
def get_store_by_name(name):
    for store in stores:
        if(store["name"]    ==  name):
            return(store)
    return jsonify({"message"   :   "No store found!"}) 

# POST - /store/<string:name>/items : add item to a specific store
@app.route('/store/<string:name>/items', methods=["POST"])
def create_new_store_item(name):
    req_data = request.get_json()
    for store in stores:
        if(store["name"]    ==  name):
            new_item = {
                'name'  :   req_data['name'],
                'price' :   req_data['price']
            }
        store['items'].append(new_item)
        return (new_item)
    return jsonify({"message"    :   "No store found"})


#GET - /store/<string:name>/items   : to display all items of a specific store
@app.route('/store/<string:name>/items')
def get_items(name):
    for store in stores:
        if(store["name"]    ==  name):
            return(jsonify({"items"   :   store["items"]}))

    return jsonify({"message"   :   "No store found"})

app.run(port=5000)