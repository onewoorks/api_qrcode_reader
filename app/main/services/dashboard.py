from ..models.customer import CustomerModel
from ..models.attended import AttendedModel
from ..models.registered_person import RegisteredPersonModel

import json

class DashboardServices:

    def get_statistic(self):
        sitting = CustomerModel().read_sitting_zone_summary()
        sit_zone = {}
        total_attend = 0
        total_total = 0
        for sit in sitting:
            sit_zone[sit['sitting']] = {
                "attend"    : "{:,.0f}".format(sit['total_attend']),
                "total"     : "{:,.0f}".format(sit['total_registered'])
            }
            total_attend += sit['total_attend']
            total_total += sit['total_registered']
        sit_zone['total'] = {
            "attend": "{:,.0f}".format(total_attend),
            "total" : "{:,.0f}".format(total_total)
        }
        return {
            "sitting_zone" : sit_zone,
        }

    def get_sitting_zone_list(self, zone):
        attendee = AttendedModel().get_attended_list(zone)
        attendee_list = []
        for a in attendee:
            data = json.loads(a['reader_payloads'])
            data['clock_in'] = str(a['clock_in'])
            attendee_list.append(data)
        return {
            "sitting_zone_list" : attendee_list
        }

    def get_manual_register(self):
        
        register_stat = []
        for r in range(4):
            registered = RegisteredPersonModel().get_register_count(r)
            result = {
                "status": r,
                "total" : registered[0]['total'],
                "vip" : "{0:,.0f}".format(int(registered[0]['vip']) if registered[0]['vip'] != None else 0),
                "normal" : "{0:,.0f}".format(int(registered[0]['normal']) if registered[0]['normal'] != None else 0),
                "clean_vip": int(registered[0]['vip']  if registered[0]['vip'] != None else 0),
                "clean_normal" : int(registered[0]['normal']  if registered[0]['normal'] != None else 0)
            }
            register_stat.append(result)
        return register_stat