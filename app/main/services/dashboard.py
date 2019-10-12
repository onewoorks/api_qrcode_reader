from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

import json

class DashboardServices:

    def GetStatistic(self):
        total_zone = CustomerModel().ReadTotalSittingZone()
        customers = CustomerModel().ReadAllCustomer()
        attended = AttendedModel().ReadAttendedCustomer()
        return {
            "sitting_zone" : total_zone,
            "customer" : json.loads(json.dumps(customers, default=str)),
            "attended" : attended
        }
