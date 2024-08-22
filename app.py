from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake, DEFAULT_IMAGE_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/')
def show_cupcakes():
    """Render homepage with an empty list for cupcakes and a form to add cupcakes."""
    return render_template("index.html")


@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Return all cupcakes in the database."""
    cupcakes = Cupcake.query.all()
    serialized = [{
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    } for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Return data for a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake and return it."""
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=float(data['rating']),
        image=data.get('image', DEFAULT_IMAGE_URL)  # Use DEFAULT_IMAGE_URL here
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = {
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image
    }

    return jsonify(cupcake=serialized), 201


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the given id."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake with the given id."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"message": "Deleted"})
