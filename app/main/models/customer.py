from . import Models

class CustomerModel:

    def read_customer_by_id(self, customer_id):
        query = "SELECT * FROM customer WHERE id = '{}' ".format(int(customer_id))
        return Models().MySqlExecuteQuery(query)
    
    def read_customer_by_code(self, code):
        query = "SELECT * FROM customer_real WHERE code = '{}' ".format(str(code))
        return Models().MySqlExecuteQuery(query)

    def read_all_customer(self):
        query = "SELECT * FROM customer"
        return Models().MySqlExecuteQuery(query)

    def read_sitting_zone_summary(self):
        query = "SELECT c.sitting, "
        query += "sum(IF(a.id is null, 0, 1)) as total_attend, "
        query += "count(c.id) as total_registered "
        query += "FROM customer_real c "
        query += "LEFT JOIN attended a on c.id = a.customer_id "
        query += "group by c.sitting "
        return Models().MySqlExecuteQuery(query)
    
    def check_attend_registered(self, customer_id):
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

    def customer_summary(self):
        query = "SELECT sitting FROM customer_real GROUP BY sitting"
        return Models().MySqlExecuteQuery(query)