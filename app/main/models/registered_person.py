from . import Models

class RegisteredPersonModel:

    def create_new_person(self, person_data):
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
        query += "'{}' ".format(person_data['ticket_price']['mode'])
        query += "); "
        return Models().execute_bulk_insert(query)

    def get_registered_person(self, register_code):
        query = "SELECT p.*, "
        query += "e.event_code, "
        query += "e.event_ref, "
        query += "e.charges "
        query += "from registered_person p "
        query += "left join event_detail e ON e.id = p.event_id "
        query += "where p.register_code = '{}' ".format(register_code)
        return Models().mysql_execute_query(query)

    def get_register_count(self, current_status):
        query = "SELECT "
        query += "'{}' as current_status ".format(current_status)
        query += ", COUNT(id) AS total "
        query += ", SUM(IF(register_mode = 'Oyoshi VIP Rock Zone', 1,0)) AS vip "
        query += ", SUM(IF(register_mode = 'Oyoshi Zone', 1,0)) AS normal "
        query += "FROM registered_person "
        if(current_status != 0):
            query += "WHERE current_status = '{}' ".format(current_status)
        return Models().mysql_execute_query(query)

    def get_register_person(self, id, register_code):
        query = "SELECT * FROM registered_person WHERE id = {} AND register_code = '{}' ".format(int(id), register_code)
        return Models().mysql_execute_query(query)