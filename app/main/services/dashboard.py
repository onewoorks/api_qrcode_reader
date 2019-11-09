from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

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
