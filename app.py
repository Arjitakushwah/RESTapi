from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_db.sqlite3"
db = SQLAlchemy(app)
api = Api(app)
app.app_context().push()

class Brand(db.Model):
    b_id = db.Column(db.Integer, primary_key = True)
    b_name = db.Column(db.String(30) , nullable = False)
    cars= db.relationship("Car", backref = "company")

class Car(db.Model):
    c_id = db.Column(db.Integer, primary_key = True)
    c_name = db.Column(db.String(30), nullable = False)
    maker= db.Column(db.Integer, db.ForeignKey("brand.b_id"))

parser = reqparse.RequestParser()
parser.add_argument("b_name")

class BrandApi(Resource): #this class will deal with crud opertions on brand class
    def get(self):
        all_brand_obj = Brand.query.all()
        i = 1
        all_brand = {}
        for brand in all_brand_obj:
            this_brand = {}
            this_brand['brand_id'] = brand.b_id
            this_brand['brand_name'] = brand.b_name
            all_brand[f'brand_{i}'] = this_brand
            i+=1
        return all_brand
    
    def post(self):
        args = parser.parse_args()
        
        new_brand = Brand(b_name = args["b_name"])
        db.session.add(new_brand)
        db.session.commit()
        return{
            "message" : "resource added successfully"
        }, 201
    def put(self, brand_id):
        args = parser.parse_args()
        this_brand = Brand.query.get(brand_id)
        this_brand.b_name = args["b_name"]
        db.session.commit()
        return{
            "message" : "resource updated successfully"
        }
    
    def delete(self, brand_id):
        this_brand = Brand.query.get(brand_id)
        db.session.delete(this_brand)
        db.session.commit()
        return {
            "message" : "resource deleted successfully"
        }


api.add_resource(BrandApi, "/api/all_brands", "/api/add_brand", "/api/update_brand/<brand_id>")

app.run(debug = True)


