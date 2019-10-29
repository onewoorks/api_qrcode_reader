from flask_restplus import Namespace, Resource, fields
from flask import (Flask, Response)
#
from ..services.dashboard import DashboardServices

import time, json, random

api = Namespace("dashboard",description="Dashboard for attendance status")

@api.route('/statistic')
class DashboardStatisticRoute(Resource):
    @api.doc("Current statistic for attendance confirmation")
    def get(self):
        data = DashboardServices().get_statistic()
        return data


@api.route('/stream-test')
class DashboardStreamTestRoute(Resource):
    statistic = DashboardServices().get_statistic()
    def get(self):
        return Response(self.event_stream(), mimetype="text/event-stream")

    def event_stream(self):
        print(self.statistic['sitting_zone'])
        while True:
            time.sleep(2)
            zone_a = random.randint(1,40)
            zone_b = random.randint(1,90)
            zone_c = random.randint(1,100)
            zone_d = random.randint(1,70)
            zone_e = random.randint(1,9)
            total_zone = zone_a + zone_b + zone_c + zone_d + zone_e
            message = {
                "attendance" : {
                    "name" : "aa",
                    "counter" : random.randint(1,15),
                    "time"  : "2019-10-22 10:47:00",
                    "zone" : chr(random.randrange(65,68))
                },
                "zone" : {
                    "A" : {
                        "present" : zone_a,
                        "total" : 40
                    },
                    "B" : {
                        "present" : zone_b,
                        "total" : 90,
                    },
                    "C" : {
                        "present" : zone_c,
                        "total" : 100
                    },
                    "D" : {
                        "present" : zone_d,
                        "total" :70
                    },
                    "E" : {
                        "present" : zone_e,
                        "total" :70
                    },
                    "TOTAL" : {
                        "present" : total_zone,
                        'total'     : 40 + 90 + 100 + 70
                    }

                }
            }
            # print("Sending {}".format(json.dumps(message)))
            yield "data: {}\n\n".format(json.dumps(message))