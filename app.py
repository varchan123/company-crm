from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    poc_name = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String(100), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    
    #__table_args__ = (db.UniqueConstraint('name', 'poc_name', 'email', name='unique_poc_combo'),)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all')
def all_companies():
    companies = Company.query.all()
    data = [{'id': c.id, 'name': c.name, 'poc_name': c.poc_name, 
             'designation': c.designation, 'mobile': c.mobile, 'email': c.email} for c in companies]
    return jsonify({'results': data, 'count': len(data)})

@app.route('/search/<name>')
def search_company(name):
    companies = Company.query.filter(Company.name.ilike(f'%{name}%')).all()
    data = [{'id': c.id, 'name': c.name, 'poc_name': c.poc_name, 
             'designation': c.designation, 'mobile': c.mobile, 'email': c.email} for c in companies]
    return jsonify({'results': data, 'count': len(data)})

@app.route('/add', methods=['POST'])
def add_company():
    data = request.json
    new_company = Company(
        name=data['name'], poc_name=data['poc_name'], 
        designation=data['designation'], mobile=data['mobile'], email=data['email']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Added successfully', 'id': new_company.id}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def update_company(id):
    company = Company.query.get_or_404(id)
    data = request.json
    company.name = data.get('name', company.name)
    company.poc_name = data.get('poc_name', company.poc_name)
    company.designation = data.get('designation', company.designation)
    company.mobile = data.get('mobile', company.mobile)
    company.email = data.get('email', company.email)
    db.session.commit()
    return jsonify({'message': 'Updated successfully'})

# Create tables on startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)