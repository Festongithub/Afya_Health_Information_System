from  flask_login import current_user, login_user
from AfyaBoraApp import app
from AfyaBoraApp.models import Doctor, Client, HealthProgram, HealthSystem
import requests


@app.route('/')
@app.route('/index')
def index():
    return "<h2> Hello world </h2>"
 

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    doctor = Doctor.query.filter_by(doctorname=data.get('doctorname')).first()
    if doctor and check_password_hash(doctor.password_hash, data.get('password')):
        return  jsonify({"message": "Login successful", "doctor_id":doctor.id}), 200
    return jsonify({"Error : Invalid credentials"}), 401


@app.route('/api/programs', methods=['POST'])
def create_program():
    data = request.get_json()
    try:
        client = HealthSystem.build_program(data.get('name'), data.get('description'))
        return jsonify({
            "id": program_id, 
            "name": program.name,
            "description": program.description
        })
    except ValueError as e:
        return jsonify({
            "error": str(e)
            }), 400

@app.route("/api/clients", methods=['POST'])
def register_client():
    data = request.get_json()
    try:
        client = HealthSystem.client_enrollment(data.get('client_id'), data.get('program_id'))
        return jsonify({
            "message": f'Client enrolled in program'
            }), 200
    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.route('/api/clients')
def search_clients():
    query = request.args.get('query', '')
    clients = HealthSystem.search_clients(query)
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "age": c.age,
        "gender": c.gender
    } for c in clients]), 200


@app.route('/api/clients/<client_id>', methods=['GET'])
def get_client_profile(client_id):
    try:
        client = HealthSystem.get_client_profile(client_id)
        return jsonify({
            "id": client.id,
            "name": client.name,
            "age": client.age,
            "gender": client.gender,
            "enrolled_programs": [{
                "id": p.id,
                "name": p.name
            } for p in client.enrolled_programs]
        }), 200
    except ValueError as e:
        return jsonify({
            "error": str(e)
            }), 404