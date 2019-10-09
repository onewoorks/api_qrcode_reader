from flask_restplus import Namespace, Resource, fields
from flask import Response
import time

api = Namespace("attendence",description="Attendence")

@api.route('/find/<qr_code>')
class FindQRCodeRoute(Resource):
    @api.doc('Find QR')
    def get(self, qr_code):
        return {
            "result":"sdfsf"
        }

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