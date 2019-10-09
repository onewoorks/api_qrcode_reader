from flask_restplus import Api

from .attendence import api as attendence_api

api = Api(
    title="Attendence Base On QR",
    version="1.0",
    description="An API for related qr attendence <style>.models {display: none !important}</style>"
)

api.add_namespace(attendence_api)

