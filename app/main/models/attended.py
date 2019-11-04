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