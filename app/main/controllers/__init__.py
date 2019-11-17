from flask_restplus import Api

from .attendence import api as attendence_api
from .dashboard import api as dashboard_api
from .register_person import api as person_register_api
from .event_detail import api as event_detail_api

api = Api(
    title="Attendence Base On QR",
    version="1.0",
    description="An API for related qr attendence <style>.models {display: none !important}</style>"
)

api.add_namespace(dashboard_api)
api.add_namespace(attendence_api)
api.add_namespace(person_register_api)
api.add_namespace(event_detail_api)