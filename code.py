from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route("/products", methods=["GET"])
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {}
        product_data["id"] = product.id
        product_data["name"] = product.name
        product_data["price"] = product.price
        product_data["quantity"] = product.quantity
        output.append(product_data)
    return jsonify({"products": output})

@app.route("/products/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    product_data = {}
    product_data["id"] = product.id
    product_data["name"] = product.name
    product_data["price"] = product.price
    product_data["quantity"] = product.quantity
    return jsonify({"product": product_data})

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(name=data["name"], price=data["price"], quantity=data["quantity"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201

@app.route("/products/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    data = request.get_json()
    product.name = data["name"]
    product.price = data["price"]
    product.quantity = data["quantity"]
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
