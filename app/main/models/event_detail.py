from . import Models

class EventDetailModel:
    def get_event_detail(self, event_id):
        query = "SELECT * FROM event_detail WHERE id = {} LIMIT 1".format(int(event_id))
        return Models().MySqlExecuteQuery(query)

    def get_event_detail_by_code(self, event_code):
        query = "SELECT * FROM event_detail WHERE event_code = '{}' LIMIT 1".format(event_code)
        return Models().MySqlExecuteQuery(query)