from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

from datetime import datetime
import json

class AttendanceServices:

    paging_total = 0

    def add_total_attendance(self):
        print('masuk je')
        self.paging_total += 1

    def get_current_stat(self):
        return self.paging_total

    def GetAllCustomers(self):
        customers = CustomerModel().ReadAllCustomer()
        for key, value in enumerate(customers):
            customers[key]['register_date'] = str(customers[key]['register_date'])
        return customers

    def read_customer_by_code(self, customer_id):
        customer = CustomerModel().read_customer_by_code(customer_id)[0]
        customer['register_date'] = str(customer['register_date'])
        return customer

    def read_customer_by_code_all(self, customer_id):
        customer = CustomerModel().read_customer_by_code(customer_id)
        for c in customer:
            c['register_date'] = str(c['register_date'])
        return customer

    def check_valid_customer(self, customer_id):
        customer = CustomerModel().check_registered_customer(customer_id)
        status = {}

        if len(customer) > 1 :
            status['code']  = 950
            status['message'] = "Proceed to Register Counter",
            status['detail'] = "duplicate qrcode found!"
        else:
            if customer[0]['attend_status'] == 0:
                status['code']      = 991
                status['message']   = "Proceed To Confirmation"
                status['detail']    = self.read_customer_by_code(customer_id)
            else:
                customer['register_date'] = str(customer['register_date'])
                status['code']      = 900
                status['message']   = "Attendance already recorded"
                status['detail']    = customer 
        return status


    def post_attendance_confirmation(self, input_data):
        payloads = {
            "customer_id"   : input_data['id_number'],
            "counter_id"    : input_data['reader_counter'],
            "reader_payloads" : json.dumps(input_data)
        }
        AttendedModel().CreateConfirmAttend(payloads)
        self.__write_stream_attendee(payloads)
        return {
            "status" : "Data registered"
        }

    def __write_stream_attendee(self, payloads):
        f = open("app/main/stream/attendee.txt", "a+")
        data = json.loads(payloads['reader_payloads'])
        data['attend_time'] = str(datetime.now()).split(".")[0]
        f.write(json.dumps(data)+"\n")
        f.close()