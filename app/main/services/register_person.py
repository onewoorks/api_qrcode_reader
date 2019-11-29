import time, json
import pandas as pd

from ..models.registered_person import RegisteredPersonModel

class RegisterPersonServices:
    def register_new_person(self, payloads):
        registered_model    = RegisteredPersonModel()
        register_code       = str(round(time.time() * 1000))
        for payload in payloads:
            payload['qr_code']        = ""
            payload['register_code']  = register_code
            registered_model.create_new_person(payload)
        return self.register_response_code(register_code)

    def register_response_code(self, register_code):
        responses = RegisteredPersonModel().get_registered_person(register_code)
        str_output = []
        for r in responses:
            r['timestamp']  = str(r['timestamp'])
            r['qr_code']   = str(r['event_ref']) + ' - ' + str(r['id']).zfill(5)
            r['charges']    = self.__show_charges(json.loads(r['charges']), r['register_mode'])
            str_output.append(r)
        return str_output

    def check_valid_person(self, person_qr):
        qr = person_qr.split('-')
        register_code = qr[-1]
        person_id = qr[-2]
        customer = RegisteredPersonModel().get_register_person(person_id, register_code)
        status = {}
        if len(customer) > 1 :
            status['code']  = 950
            status['message'] = "Proceed to Register Counter",
            status['detail'] = "duplicate qrcode found!"
        else:
            if 0 < len(customer):
                customer[0]['timestamp'] = str(customer[0]['timestamp'])
                customer[0]['current_status'] = self.__current_status_label(customer[0]['current_status'])
                status['code']      = 991
                status['message']   = "Proceed To Confirmation"
                status['detail']    = customer[0]
            else:
                status['code']     = 950
                status['message']  = "QR Code not found!!"
                status['detail']   = ""
        return status

    def __show_charges(self, charges_payload, register_mode):
        charge = 0
        for c in charges_payload:
            if c['mode'] == register_mode:
                charge = c['charge']
        return charge

    def __current_status_label(self, current_status):
        label = "NEXT"
        if current_status == 0:
            label = "New Register"
        if current_status == 1:
            label = "Payment Done"
        if current_status == 2:
            label = "Confirm Attend"
        return label
