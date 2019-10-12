from flask_restplus import Namespace, Resource, fields
from flask import Response, request

from ..services.dashboard import DashboardServices

import time, json

api = Namespace("dashboard",description="Dashboard for attendance status")

@api.route('/statistic')
class DashboardStatisticRoute(Resource):
    @api.doc("Current statistic for attendance confirmation")
    def get(self):
        data = DashboardServices().GetStatistic()
        return data
