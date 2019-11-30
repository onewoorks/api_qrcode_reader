from flask_restplus import Namespace, Resource, fields
from flask import (Flask, Response)
#
from ..services.dashboard import DashboardServices
from ..services.attendance import AttendanceServices

import time, json, random

api = Namespace("dashboard",description="Dashboard for attendance status")

@api.route('/statistic')
class DashboardStatisticRoute(Resource):
    @api.doc("Current statistic for attendance confirmation")
    def get(self):
        data = DashboardServices().get_statistic()
        return data

@api.route('/sitting-zone/<sitting_zone>')
class DashboardSittingZoneRoute(Resource):
    def get(self, sitting_zone):
        data = DashboardServices().get_sitting_zone_list(sitting_zone)
        return data

    def event_stream(self):
        f = open('app/main/stream/attendee_zone.txt', 'r')
        attendance = []
        attendee = f.readlines()
        for a in attendee:
            attendance.append(json.loads(a))
        f.close()
        open('app/main/stream/attendee.txt', 'w').close()
        statistic = DashboardServices().get_statistic()
        dashboard = {
            "zone" : statistic['sitting_zone'],
            "attendance" : attendance
        }
        yield "data: {}\n\n".format(json.dumps(dashboard))

@api.route('/stream-stat')
class DashboardStreatStatRoute(Resource):
    def get(self):
        return Response(self.event_stream(), mimetype="text/event-stream")
    
    def event_stream(self):
        f = open('app/main/stream/attendee.txt', 'r')
        attendance = []
        attendee = f.readlines()
        for a in attendee:
            attendance.append(json.loads(a))
        f.close()
        open('app/main/stream/attendee.txt', 'w').close()
        statistic = DashboardServices().get_statistic()
        dashboard = {
            "zone" : statistic['sitting_zone'],
            "attendance" : attendance
        }
        yield "data: {}\n\n".format(json.dumps(dashboard))

@api.route('/stream-manual-register')
class DashboardStreatStatRoute(Resource):
    def get(self):
        return Response(self.event_stream(), mimetype="text/event-stream")
    
    def event_stream(self):
        statistic = DashboardServices().get_manual_register()
        paid_vip = 0
        paid_normal = 0
        total_paid = 0
        for s in statistic:
            if s['status'] > 1:
                paid_vip += s['clean_vip'] * 135
                paid_normal += s['clean_normal'] * 80
                total_paid += 1

        dashboard = {
            "statistic" : statistic,
            "collection" : {
                "total": total_paid,
                "vip": paid_vip,
                "normal": paid_normal
            }
        }
        yield "data: {}\n\n".format(json.dumps(dashboard))

@api.route('/stream-test')
class DashboardStreamTestRoute(Resource):
    statistic = DashboardServices().get_statistic()
    def get(self):
        return Response(self.event_stream(), mimetype="text/event-stream")

    def event_stream(self):
        open('app/main/stream/demofile2.txt', 'w').close()
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
            yield "data: {}\n\n".format(json.dumps(message))
