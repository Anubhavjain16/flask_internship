from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
    test_duration = db.Column(db.Integer, nullable=False)
    test_category = db.Column(db.String(100), nullable=False)
    test_difficulty = db.Column(db.String(100), nullable=False)
    test_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Test {self.id} {self.test_name}>'

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_name = request.form['name']
        test_duration = request.form['duration']
        test_category = request.form['category']
        test_difficulty = request.form['difficulty']
        test_description = request.form['description']
        new_test = Test(
            test_name=test_name,
            test_duration=test_duration,
            test_category=test_category,
            test_difficulty=test_difficulty,
            test_description=test_description
        )

        try:
            db.session.add(new_test)
            db.session.commit()
            return 'Test added successfully!'
        except IntegrityError:
            db.session.rollback()
            return 'Test with the same name already exists. Choose a different name.'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
