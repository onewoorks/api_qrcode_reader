from . import Models

class AttendedModel:
    
    def CreateConfirmAttend(self, payloads):
        query = "INSERT INTO attended (customer_id, counter_id, reader_payloads) VALUE "
        query += "("
        query += "'{}', ".format(payloads['customer_id'])
        query += "'{}', ".format(payloads['counter_id'])
        query += "'{}'".format(payloads['reader_payloads'].replace("'","''"))
        query += ")"
        Models().mysql_insert_query(query)

    def ReadAttendedCustomer(self):
        query = "SELECT count(id) AS total, "
        query += "reader_payloads->>\"$.sitting_zone\" AS sitting_zone "
        query += "FROM attended "
        query += "GROUP BY reader_payloads->>\"$.sitting_zone\" "
        return Models().mysql_execute_query(query)

    def get_attended_list(self, zone):
        query = "SELECT date_format(timestamp,'%d/%m/%Y %H:%i:%s') as clock_in, "
        query += "reader_payloads "
        query += "FROM attended WHERE reader_payloads->>'$.sitting_zone' = '{}'".format(zone)
        return Models().mysql_execute_query(query)

    def get_customer_filter(self, filter_data):
        query = "SELECT c.*, "
        query += "(SELECT count(id) as total from attended where customer_id = c.id) as 'attended' "
        query += "FROM customer_real c "
        query += "WHERE 1 "
        query += "AND c.code = '{}' ".format(filter_data['qr_code']) if filter_data['qr_code'] != None else ""
        query += "AND c.phone LIKE \"%{}\" ".format(filter_data['phone']) if filter_data['phone'] != None else ""
        query += "AND c.name LIKE \"%{}%\" ".format(filter_data['name']) if filter_data['name'] != None else ""
        query += "AND c.email LIKE '%{}%' ".format(filter_data['email'])  if filter_data['email'] != None else ""
        print(query)
        return Models().mysql_execute_query(query)