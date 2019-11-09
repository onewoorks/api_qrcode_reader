from . import Models

class AttendedModel:
    
    def CreateConfirmAttend(self, payloads):
        query = "INSERT INTO attended (customer_id, counter_id, reader_payloads) VALUE "
        query += "("
        query += "'{}', ".format(payloads['customer_id'])
        query += "'{}', ".format(payloads['counter_id'])
        query += "'{}'".format(payloads['reader_payloads'].replace("'","''"))
        query += ")"
        Models().MysqlInsertQuery(query)

    def ReadAttendedCustomer(self):
        query = "SELECT count(id) AS total, "
        query += "reader_payloads->>\"$.sitting_zone\" AS sitting_zone "
        query += "FROM attended "
        query += "GROUP BY reader_payloads->>\"$.sitting_zone\" "
        return Models().MySqlExecuteQuery(query)

    def get_attended_list(self, zone):
        query = "SELECT date_format(timestamp,'%d/%m/%Y %H:%i:%s') as clock_in, "
        query += "reader_payloads "
        query += "FROM attended WHERE reader_payloads->>'$.sitting_zone' = '{}'".format(zone)
        print(query)
        return Models().MySqlExecuteQuery(query)

    def get_customer_filter(self, filter_data):
        query = "SELECT * FROM customer_real "
        query += "WHERE 1 "
        query += "AND CODE = '{}' ".format(filter_data['qr_code']) if filter_data['qr_code'] != None else ""
        query += "AND phone LIKE \"%{}\" ".format(filter_data['phone']) if filter_data['phone'] != None else ""
        query += "AND NAME LIKE \"%{}%\" ".format(filter_data['name']) if filter_data['name'] != None else ""
        query += "AND email LIKE '%{}' ".format(filter_data['email'])  if filter_data['email'] != None else ""
        return Models().MySqlExecuteQuery(query)