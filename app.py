from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Jose'
api = Api(app)
jwt = JWT(app, authenticate, identity)

students = []


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Address',
                        type=str,
                        required=True,
                        help='Address is required')
    parser.add_argument('Alma_mater',
                        type=str,
                        required=True,
                        help='Alma mater is required')

    @jwt_required()
    def get(self, name):
        student = next(filter(lambda x: x['name'] == name, students), None)
        return {'student': student}, 200 if student is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, students), None):
            return {'error_message': 'Student already exists.'}, 400
        data = Student.parser.parse_args()
        student = {'name': name, 'Address': data['address'], 'Alma_mater': data['alma_mater']}
        students.append(student)
        return student, 201

    def delete(self, name):
        global students
        students = list(filter(lambda x: x['name'] != name, students))
        return students

    def put(self, name):
        student = next(filter(lambda x: x['name'] == name, students), None)
        if student is None:
            return {'error_message': 'Student does not exist.'}, 404
        data = Student.parser.parse_args()
        student.update(data)
        return student


class StudentList(Resource):
    def get(self):
        return students


api.add_resource(Student, '/student/<name>')
api.add_resource(StudentList, '/students')

app.run(port=5000, debug=True)


