from . import Models

class CustomerModel:

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