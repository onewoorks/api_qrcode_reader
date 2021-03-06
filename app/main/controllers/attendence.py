from flask_restplus import Namespace, Resource, fields
from flask import Response, request

from ..services.attendance import AttendanceServices
from ..services.register_person import RegisterPersonServices

import time, json

api = Namespace("attendence",description="Attendence")

@api.route('/find-all/<qr_code>')
class AttendanceFindAllRoute(Resource):
    def get(self, qr_code):
        data = AttendanceServices().read_customer_by_code_all(qr_code)
        return data

@api.route('/find/<qr_code>')
class FindQRCodeRoute(Resource):
    @api.doc('Find customer detail by QR Code')
    def get(self, qr_code):
        data = AttendanceServices().check_valid_customer(qr_code)
        return data

model_filter = api.model('Filter Information',{
    "name"      : fields.String(description="Registered Name"),
    "qr_code"   : fields.String(description="QR Code"),
    "email"     : fields.String(description="Registered Email"),
    "phone"     : fields.String(description="Registered Phone No")
})

@api.route('/find-person/<qr_code>')
class FindQRCodeRoute(Resource):
    @api.doc('Find customer detail by QR Code')
    def get(self, qr_code):
        data = RegisterPersonServices().check_valid_person(qr_code)
        return data

@api.route('/find-filter')
class AttendanceFindFilter(Resource):
    def post(self):
        input_data = json.loads(request.data)
        response = AttendanceServices().post_filter_registered_customer(input_data)
        return response

info_attendance = api.model('Attendance Information',{
    "customer_name"     : fields.String(description="Customer Name"),
    "customer_phone_no" : fields.String(description="Customer Phone No"),
    "email"             : fields.String(description="Customer Email"),
    "register_date"     : fields.String(description="Register Date"),
    "reader_counter"    : fields.String(description="Perform Counter"),
    "sitting_zone"      : fields.String(description="Sitting Zone"),
    "id_number"         : fields.String(description="Id Data as in database table"),
    "qr_code"           : fields.String(description="QR Code")
})
@api.route('/attend')
class AttendRoute(Resource):
    @api.doc('Registrant confirm their attendance')
    @api.doc(parser=info_attendance)
    def post(self):
        input_data  = json.loads(request.data)
        response = AttendanceServices().post_attendance_confirmation(input_data)
        return response

@api.route('/next-status')
class AttendRoute(Resource):
    @api.doc('Next Status Confirmation')
    @api.doc(parser=info_attendance)
    def post(self):
        input_data  = json.loads(request.data)
        response = AttendanceServices().post_confirmation_trail(input_data)
        return response
    
@api.route('/attend-manual')
class AttendRoute(Resource):
    @api.doc('Registrant confirm their attendance')
    @api.doc(parser=info_attendance)
    def post(self):
        print(json.loads(request.data))
        input_data  = json.loads(request.data)
        input_data['customer_name'] = input_data['name']
        input_data['sitting_zone'] = input_data['sitting']
        response = AttendanceServices().post_attendance_confirmation(input_data)
        return response

@api.route('/stream')
class StreamRoute(Resource):
    @api.doc('Stream')
    def get_message(self):
        '''this could be any function that blocks until data is ready'''
        time.sleep(1.0)
        s = time.ctime(time.time())
        return s

    def get(self):
        def eventStream():
            while True:
                yield 'data: {}\n\n'.format(self.get_message())
        return Response(eventStream(), mimetype="text/event-stream")