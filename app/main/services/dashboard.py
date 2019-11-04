from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

import json

class DashboardServices:

    def get_statistic(self):
        sitting = CustomerModel().read_sitting_zone_summary()
        sit_zone = {}
        for sit in sitting:
            sit_zone[sit['sitting']] = {
                "attend"    : "{:,.0f}".format(sit['total_attend']),
                "total"     : "{:,.0f}".format(sit['total_registered'])
            }
        return {
            "sitting_zone" : sit_zone,
        }
