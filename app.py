from flask import Flask,render_template,redirect,request, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
import json 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Person(db.Model, JsonModel):
    __tablename__ = 'persons'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

'''create table, and drop table if exists'''


@app.route('/todos/create',methods=['POST'])
def create_todos():
    description = request.get_json()['name']
    todo = Person(name = description)
    db.session.add(todo)
    db.session.commit()
    #return redirect(url_for('index'))
    return jsonify({
        'name': todo.name
    })

@app.route('/todos/get', methods=['POST'])
def get_todos():
    person = Person.query.all()
    return json.dumps([u.as_dict() for u in Person.query.all()])


db.create_all()
@app.route('/')
def index():
    person = Person.query.all()
    return render_template('index.html',data=person)
    #  return jsonify({
    #     'name': person.name
    #   })



if __name__ == '__main__':
    app.run()
