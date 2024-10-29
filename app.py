from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from flask_migrate import Migrate
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
migrate = Migrate(app, db)


connect_db(app)
def init_db():
    with app.app_context():
        db.create_all()
        
init_db()

@app.route('/')
def list_pets():
    pets = Pet.query.all()
    print([(pet.name, pet.photo_url) for pet in pets])# This will fetch all pets from the database once it's set up.
    return render_template('home.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Display form to add a pet and handle form submission."""
    form = AddPetForm()
    
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=form.available.data)
        
        db.session.add(new_pet)
        db.session.commit()
        
        flash(f"Added {name} the {species}")
        return redirect('/')
    else:
        return render_template('add_pet_form.html', form=form)
    
    
@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Show details about a single pet, and allow for editing that pet."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        
        flash(f"Updated {pet.name} the {pet.species}")
        return redirect('/')
    else:
        # if the form isn't being submitted (i.e. if it's a GET request), then just render the template
        return render_template('edit_pet.html', form=form, pet=pet)