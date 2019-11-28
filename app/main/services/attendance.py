from ..models.customer import CustomerModel
from ..models.attended import AttendedModel

from datetime import datetime, timedelta
import json

class AttendanceServices:

    paging_total = 0

    def add_total_attendance(self):
        self.paging_total += 1

    def get_current_stat(self):
        return self.paging_total

    def get_all_customer(self):
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
            if 0 < len(customer):
                if customer[0]['attend_status'] == 0:
                    status['code']      = 991
                    status['message']   = "Proceed To Confirmation"
                    status['detail']    = self.read_customer_by_code(customer_id)
                else:
                    customer['register_date'] = str(customer['register_date'])
                    status['code']      = 900
                    status['message']   = "Attendance already recorded"
                    status['detail']    = customer 
            else:
                status['code']     = 950
                status['message']  = "QR Code not found!!"
                status['detail']   = ""
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

    def post_confirmation_trail(self, input_data):
        payloads = {
            "customer_id"   : input_data['id_number'],
            "reader_payloads" : json.dumps(input_data)
        }
        AttendedModel().create_confirm_trail(payloads)
        return {
            "status" : "Trail Registered"
        }
    

    def post_filter_registered_customer(self, filter_data):
        valid = False
        for fd in filter_data:
            if fd == "qr_code":
                if len(filter_data[fd]) > 0 :
                    valid = True
                else:
                    filter_data[fd] = None
            else:
                if len(filter_data[fd]) > 4:
                    valid = True
                else:
                    filter_data[fd] = None
        if valid == True:
            found = AttendedModel().get_customer_filter(filter_data)
            result = found if len(found) > 0 else {"status":"No entry found!!!"}
        else:
            result = {
                "status" : "No entry found!!!"
            }
        return result

    def __write_stream_attendee(self, payloads):
        f = open("app/main/stream/attendee.txt", "a+")
        data = json.loads(payloads['reader_payloads'])
        dt = datetime.now() + timedelta(hours=8)
        data['attend_time'] = str(dt).split(".")[0]
        f.write(json.dumps(data)+"\n")
        f.close()