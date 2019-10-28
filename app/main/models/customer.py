from . import Models

class CustomerModel:

    def ReadCustomerById(self, customer_id):
        query = "SELECT * FROM customer WHERE id = '{}' ".format(int(customer_id))
        return Models().MySqlExecuteQuery(query)
    
    def read_customer_by_code(self, code):
        query = "SELECT * FROM customer_real WHERE code = '{}' ".format(str(code))
        return Models().MySqlExecuteQuery(query)

    def ReadAllCustomer(self):
        query = "SELECT * FROM customer"
        return Models().MySqlExecuteQuery(query)

    def ReadTotalSittingZone(self):
        query = "SELECT sitting_zone, count(id) as total_registered_customer "
        query += "FROM customer GROUP BY sitting_zone"
        return Models().MySqlExecuteQuery(query)
    
    def CheckAttendRegistered(self, customer_id):
        query = "SELECT DISTINCT c.*, "
        query += "IF(a.id is null, 0, 1) as attend_status "
        query += "FROM customer c "
        query += "LEFT JOIN attended a on c.id=a.customer_id "
        query += "WHERE c.id = {} ".format(int(customer_id))
        return Models().MySqlExecuteQuery(query)
    
    def check_registered_customer(self, code):
        query = "SELECT DISTINCT c.*, "
        query += "IF(a.id is null, 0, 1) as attend_status "
        query += "FROM customer_real c "
        query += "LEFT JOIN attended a on c.id = a.customer_id "
        query += "WHERE c.code = '{}' ".format(str(code))
        return Models().MySqlExecuteQuery(query)