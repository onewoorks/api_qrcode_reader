from flask_restplus import Namespace, Resource, fields
from flask import Response, request

from ..services.register_person import RegisterPersonServices

import time,json

api = Namespace('register-person', description="Register New Person ")

model_person = api.model('Person Information',{
    "fullname"          : fields.String(description="Person full name"),
    "identification_no" : fields.String(description="Person General Identification No"),
    "phone_no"          : fields.String(description="Person Phone No"),
    "email"             : fields.String(description="Person Email"),
    'device_info'       : "",
    "register_mode"     : fields.String(description="Registration Mode")
})
@api.route('/new-data')
class NewDataRoute(Resource):
    @api.doc("Field required for person registration")
    @api.expect(parser= model_person)
    def post(self):
        input_data  = json.loads(request.data)
        response    = RegisterPersonServices().register_new_person(input_data)
        return response

@api.route('/register-code/<register_code>')
class RegisterCodeRoute(Resource):
    def get(self, register_code):
        return RegisterPersonServices().register_response_code(register_code)