from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

import json

class AttendanceServices:

    def GetAllCustomers(self):
        customers = CustomerModel().ReadAllCustomer()
        for key, value in enumerate(customers):
            customers[key]['register_date'] = str(customers[key]['register_date'])
        return customers

    def CheckValidCustomer(self, customer_id):
        customer = CustomerModel().CheckAttendRegistered(customer_id)[0]
        status = {}
        if customer['attend_status'] == 0:
            status['code']      = 991
            status['message']   = "Proceed To Confirmation"
            # status['detail']    = ""
        else:
            customer['register_date'] = str(customer['register_date'])
            status['code']      = 900
            status['message']   = "Attendance already recorded"
            status['detail']    = customer
        return status


    def PostAttendanceConfirmation(self, input_data):
        payloads = {
            "customer_id"   : input_data['id_number'],
            "counter_id"    : input_data['reader_counter'],
            "reader_payloads" : json.dumps(input_data)
        }
        AttendedModel().CreateConfirmAttend(payloads)
        return {
            "status" : "Data registered"
        }