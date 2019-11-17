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
            r['qr_code']   = str(r['event_code']) + ' - ' + str(r['id']).zfill(5)
            r['charges']    = self.__show_charges(json.loads(r['charges']), r['register_mode'])
            str_output.append(r)
        return str_output

    def __show_charges(self, charges_payload, register_mode):
        charge = 0
        for c in charges_payload:
            if c['mode'] == register_mode:
                charge = c['charge']
        return charge