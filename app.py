from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv(override=True)
pw = os.getenv("pw")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://postgres:{pw}@localhost/adopt'

app.app_context().push()

app.config["SECRET_KEY"] = "HELLO123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

photo = "https://st4.depositphotos.com/14953852/22772/v/600/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg"


@app.route('/')
# route for taking you home
def home_index():
    pets = Pet.query.all()
    return render_template("pet_home.html", pets=pets)


@app.route('/add', methods=["GET", "POST"])
# route for rendering add pet form 
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_URL.data or None
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species,
                  photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('add_pet_form.html', form=form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
# route for editing a pet
def edit_pet_form(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_URL.data if form.photo_URL.data else photo
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.add(pet)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('edit_pet_form.html', pet=pet, form=form)
