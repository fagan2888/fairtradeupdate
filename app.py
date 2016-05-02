import sqlite3
import uuid
from flask import Flask, g, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ftu.db'
db = SQLAlchemy(app)

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	project_id = db.Column(db.String(36), unique=True)
	project_email = db.Column(db.String(120), unique=True)
	project_name = db.Column(db.String(120))
	updates = db.relationship("PUpdate", backref="project", lazy='dynamic')

	def serialize(self):
		return {
			'id': self.project_id,
			'name': self.project_name,
			'updates': [update.serialize() for update in self.updates.all()],
			'email': self.project_email
		}

	def __init__(self, project_name, project_email):
		self.project_name = project_name
		self.project_email = project_email
		self.project_id = str(uuid.uuid4())

	def __repr__(self):
		return '<Project %r>' % self.project_name

class PUpdate(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	money = db.Column(db.String(120))
	people = db.Column(db.String(120))
	description = db.Column(db.String(500))

	def serialize(self):
		return {
			'money': self.money,
			'people': self.people,
			'description': self.description
		}

	def __init__(self, info):
		self.money = info["money"]
		self.people = info["people"]
		self.description = info["description"]

	def __repr__(self):
		return '<Update %r>' % str(self.description)

@app.route('/project/<project_id>')
def project(project_id):
	return jsonify(project=Project.query.filter_by(project_id=project_id).first().serialize())

@app.route('/submit')
def submit_project():
	p = Project(request.args.get('name'), request.args.get('email'))
	db.session.add(p)
	db.session.commit()
	return jsonify({'status': 'success'})

@app.route('/update')
def update():
	p = Project.query.filter_by(project_id=request.args.get('project_id')).first()
	u = PUpdate({
		'money': request.args.get('money'),
		'people': request.args.get('people'),
		'description': request.args.get('description')
	})
	p.updates.append(u)
	db.session.add(p)
	db.session.add(u)
	db.session.commit()
	return jsonify({'status':'success'})

@app.route('/projects')
def projects():
	return jsonify(projects=[project.serialize() for project in Project.query.all()])

if __name__ == "__main__":
	app.run(debug=True, port=5001)
