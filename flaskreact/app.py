from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow #ModuleNotFoundError: No module named 'flask_marshmallow' = pip install flask-marshmallow https://pypi.org/project/flask-marshmallow/
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flaskreact'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
 
ma=Marshmallow(app)

class Sanctions(db.Model):
    __tablename__="sanctions"
    id = db.Column(db.Integer,primary_key=True)
    student_name = db.Column(db.String(100))
    sanct_title = db.Column(db.String(100))
    sanct_desc = db.Column(db.String(200))
    sanct_hours = db.Column(db.Integer)
    date = db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,student_name,sanct_title,sanct_desc,sanct_hours):
        self.student_name=student_name
        self.sanct_title=sanct_title
        self.sanct_desc=sanct_desc
        self.sanct_hours=sanct_hours

class SanctionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'student_name', 'sanct_title', 'sanct_desc', 'sanct_hours', 'date')

sanction_schema = SanctionSchema()
sanctions_schema = SanctionSchema(many=True)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route('/listsanctions', methods=['GET'])
def listsanctions():
    all_sanctions = Sanctions.query.all()
    results = sanctions_schema.dump(all_sanctions)
    return jsonify(results)

@app.route('/sanctiondetails/<id>', methods=['GET'])
def sanctiondetails(id):
    sanction = Sanctions.query.get(id)
    return sanction_schema.jsonify(sanction)

@app.route('/sanctionupdate/<id>', methods=['PUT'])
def sanctionupdate(id):
    sanction = Sanctions.query.get(id)

    student_name = request.json['student_name']
    sanct_title = request.json['sanct_title']
    sanct_desc = request.json['sanct_desc']
    sanct_hours = request.json['sanct_hours']

    sanction.student_name = student_name
    sanction.sanct_title = sanct_title
    sanction.sanct_desc = sanct_desc
    sanction.sanct_hours = sanct_hours

    if not sanction:
        return jsonify({'message': 'Sanction not found'}), 404

    db.session.commit()
    return sanction_schema.jsonify(sanction)

@app.route('/sanctiondelete/<id>', methods=['DELETE'])
def sanctiondelete(id):
    sanction = Sanctions.query.get(id)

    if not sanction:
        return jsonify({'message': 'Sanction not found'}), 404

    db.session.delete(sanction)
    db.session.commit()

    return jsonify({'message': 'Sanction deleted successfully'}), 200

@app.route('/sanctionadd', methods=['POST'])
def sanctionadd():
    student_name = request.json['student_name']
    sanct_title = request.json['sanct_title']
    sanct_desc = request.json['sanct_desc']
    sanct_hours = request.json['sanct_hours']

    sanctions = Sanctions(student_name,sanct_title,sanct_desc,sanct_hours)
    db.session.add(sanctions)
    db.session.commit()
    return sanction_schema.jsonify(sanctions)