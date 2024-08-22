from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

CUPCAKE_DATA_UPDATE = {
    "flavor": "UpdatedFlavor",
    "size": "UpdatedSize",
    "rating": 9,
    "image": "http://test.com/updated_cupcake.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            Cupcake.query.delete()
            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        """Test listing cupcakes."""
        with app.app_context():  # Ensure context is active
            with app.test_client() as client:
                resp = client.get("/api/cupcakes")

                self.assertEqual(resp.status_code, 200)

                cupcake = Cupcake.query.first()  # Fetch the cupcake again from the database
                data = resp.json
                self.assertEqual(data, {
                    "cupcakes": [
                        {
                            "id": cupcake.id,
                            "flavor": "TestFlavor",
                            "size": "TestSize",
                            "rating": 5,
                            "image": "http://test.com/cupcake.jpg"
                        }
                    ]
                })

    def test_get_cupcake(self):
        """Test getting a single cupcake."""
        with app.app_context():  # Ensure context is active
            with app.test_client() as client:
                cupcake = Cupcake.query.first()  # Fetch the cupcake again from the database
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.get(url)

                self.assertEqual(resp.status_code, 200)
                data = resp.json
                self.assertEqual(data, {
                    "cupcake": {
                        "id": cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                })

    def test_create_cupcake(self):
        """Test creating a new cupcake."""
        with app.app_context():  # Ensure context is active
            with app.test_client() as client:
                url = "/api/cupcakes"
                resp = client.post(url, json=CUPCAKE_DATA_2)

                self.assertEqual(resp.status_code, 201)

                data = resp.json
                self.assertIsInstance(data['cupcake']['id'], int)
                del data['cupcake']['id']

                self.assertEqual(data, {
                    "cupcake": {
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image": "http://test.com/cupcake2.jpg"
                    }
                })

                self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Test updating a cupcake."""
        with app.app_context():  # Ensure context is active
            with app.test_client() as client:
                cupcake = Cupcake.query.first()
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.patch(url, json=CUPCAKE_DATA_UPDATE)

                self.assertEqual(resp.status_code, 200)

                data = resp.json
                self.assertEqual(data, {
                    "cupcake": {
                        "id": cupcake.id,
                        "flavor": "UpdatedFlavor",
                        "size": "UpdatedSize",
                        "rating": 9,
                        "image": "http://test.com/updated_cupcake.jpg"
                    }
                })

    def test_delete_cupcake(self):
        """Test deleting a cupcake."""
        with app.app_context():  # Ensure context is active
            with app.test_client() as client:
                cupcake = Cupcake.query.first()
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.delete(url)

                self.assertEqual(resp.status_code, 200)
                data = resp.json
                self.assertEqual(data, {"message": "Deleted"})

                self.assertEqual(Cupcake.query.count(), 0)
