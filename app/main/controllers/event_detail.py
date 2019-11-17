from flask_restplus import Namespace, Resource, fields
from flask import Response, request

from ..services.event_detail import EventDetailServices

api = Namespace('event', description="Event information")

@api.route('/event/<event_id>')
class EventDetailRoute(Resource):
    def get(self, event_id):
        return EventDetailServices().get_event_detail(event_id)

@api.route('/info/<event_code>')
class EventDetailRoute(Resource):
    def get(self, event_code):
        return EventDetailServices().get_event_detail_by_code(event_code)