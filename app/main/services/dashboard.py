from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

import json

class DashboardServices:

    def get_statistic(self):
        sitting = CustomerModel().read_sitting_zone_summary()
        for sit in sitting:
            sit['total_attend'] =  int(sit['total_attend'])
        
        # customers = CustomerModel().ReadAllCustomer()
        # attended = AttendedModel().ReadAttendedCustomer()
        return {
            "sitting_zone" : sitting,
            # "customer" : json.loads(json.dumps(customers, default=str)),
            # "attended" : attended
        }
