from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLite database file
db = SQLAlchemy(app)

# Define the model
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

    # Add initial data
    initial_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Eve"]
    for name in initial_names:
        existing_name = Name.query.filter_by(name=name).first()
        if not existing_name:
            new_name = Name(name=name)
            db.session.add(new_name)
    db.session.commit()


def search_name(name):
    result = Name.query.filter(func.lower(Name.name) == func.lower(name)).first()
    if result:
        return f"{name} found in the database!"
    else:
        return f"{name} not found in the database."

@app.route("/")
def index():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    name = data["name"]
    result = search_name(name)
    return jsonify({"results": [result]})

if __name__ == "__main__":
    app.run(debug=True)
