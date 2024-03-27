import os
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy
from form import AddCupcakeForm

app=Flask(__name__)
app.app_context().push()

# set environment variable to NOTTEST if were working the real DB in app.py, if we are in test mode in test.py this variable is set to "TEST" and we use the test database
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes' if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else 'postgresql:///test_cupcakes' 
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO']= True
# app.config['SQLALCHEMY_ECHO']= True if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else False
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)
#-------html routes go below --------
@app.route("/base")
def show_base():
    """show base template page for reference"""
    return render_template("base.html")

@app.route("/")
def show_home():
    """show base template page for reference"""
    form=AddCupcakeForm()
    return render_template("home.html", form=form)

@app.route("/showcupcakes")
def show_cupcakes_page():
    """show html of all our beautiful cupcakes. It's here because I can and the images are pretty good"""
    all_cupcakes=Cupcake.query.all()
    return render_template("cupcakelist.html", cupcakes=all_cupcakes)

#-------api routes go below --------
@app.route("/api/cupcakes")
def get_all_cupcakes():
    cupcakes=Cupcake.query.all()
    serialized_cupcakes=[cupcake.serialize_cupcake() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized_cupcakes)

@app.route("/api/cupcakes/<cupcake_id>")
def get_a_cupcake(cupcake_id):
    int_cupcake_id=int(cupcake_id)
    cupcake=Cupcake.query.get_or_404(int_cupcake_id)
    serialized_cupcake=cupcake.serialize_cupcake()
    return jsonify(cupcake=serialized_cupcake)

@app.route("/api/cupcakes", methods=['POST'])
def add_new_cupcake():
    print(" Checking the data we received in request.json!!!->->",request.json)
    cake_flavor=request.json["flavor"]
    cake_size=request.json["size"]
    cake_rating=request.json["rating"]
    cake_image=request.json["image"]
    new_cupcake=Cupcake(flavor=cake_flavor, size=cake_size, rating=cake_rating, image=cake_image)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized_new_cupcake=new_cupcake.serialize_cupcake()
    return (jsonify(new_cupcake=serialized_new_cupcake),201)

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def del_a_cupcake(cupcake_id):
    int_cupcake_id=int(cupcake_id)
    cupcake=Cupcake.query.get_or_404(int_cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({"message":f"Successfully Deleted Cupcake with an id of {cupcake.id}"})

#Several approaches to this patch route which I will detail.

#1 replace with all fields found in request.json. This method is good if the user doesn't want to update all fields. However, if anything doesn't conform to the model we will get a bug,which is possible.

# @app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
# def edit_a_cupcake_v1(cupcake_id):
#     print(" Checking the data we received in request.json!!!->->",request.json)
#     int_cupcake_id=int(cupcake_id)
#     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
#     Cupcake.query.filter_by(id=int_cupcake_id).update(request.json)
#     db.session.commit()
#     serialized_cupcake=cupcake.serialize_cupcake()
#     return jsonify(edited_cupcake=serialized_cupcake)

#2 Edits the existing cupcake one field/attribute at a time. A bit longer/tedious but works well given the exercises assumption that all an entire cupcake obj is passed in to the backend. 
#If this wasn't the case it could be problematic for updating just one or two fields.
@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def edit_a_cupcake_v2(cupcake_id):
    print(" Checking the data we received in request.json!!! ->->",request.json)
    int_cupcake_id=int(cupcake_id)
    cupcake=Cupcake.query.get_or_404(int_cupcake_id)
    cupcake.flavor=request.json["flavor"]
    cupcake.size=request.json["size"]
    cupcake.rating=request.json["rating"]
    cupcake.image=request.json["image"]
    db.session.commit()
    serialized_cupcake=cupcake.serialize_cupcake()
    return jsonify(edited_cupcake=serialized_cupcake)



# {
# 	"cupcake": {
# 		"flavor": "lemon",
# 		"id": 3,
# 		"image": "https://tinypic.host/images/2024/03/25/vegan-lemon-cupcakes-1..jpeg",
# 		"rating": 7.0,
# 		"size": "small"
# 	}
# }








