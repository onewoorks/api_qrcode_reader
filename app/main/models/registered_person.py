from . import Models

class RegisteredPersonModel:

    def create_new_person(self, person_data):
        print(person_data)
        query = "INSERT INTO registered_person "
        query += "(timestamp, fullname, identification_no, phone_no, email, event_id,"
        query += "qr_code, register_code, register_mode) VALUE ( now(), "
        query += "'{}', ".format(person_data['fullname'])
        query += "'{}', ".format(person_data['identification_no'])
        query += "'{}', ".format(person_data['phone_no'])
        query += "'{}', ".format(person_data['email'])
        query += "'{}', ".format(person_data['event_id'])
        query += "'{}', ".format(person_data['qr_code'])
        query += "'{}', ".format(person_data['register_code'])
        query += "'{}' ".format(person_data['register_mode'])
        query += "); "
        return Models().execute_bulk_insert(query)

    def get_registered_person(self, register_code):
        query = "SELECT p.*, "
        query += "e.event_code, "
        query += "e.charges "
        query += "from registered_person p "
        query += "left join event_detail e ON e.id = p.event_id "
        query += "where p.register_code = '{}' ".format(register_code)
        return Models().MySqlExecuteQuery(query)