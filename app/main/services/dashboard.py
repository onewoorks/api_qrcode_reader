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
        registered = RegisteredPersonModel().get_register_count()
        register_stat = []
        for r in registered:
            result = {
                r['current_status'] : r['total']
            }
            register_stat.append(result)
        return register_stat
