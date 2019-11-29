import json

from ..models.event_detail import EventDetailModel

class EventDetailServices:
    def get_event_detail(self, event_id):
        response = EventDetailModel().get_event_detail(int(event_id))
        output = []
        for r in response:
            r['timestamp'] = str(r['timestamp'])
            r['charges'] = json.loads(r['charges'])
            output.append(r)
        return output[0]

    def get_event_detail_by_code(self, event_code):
        response = EventDetailModel().get_event_detail_by_code(event_code)
        output = []
        if len(response)>0:
            for r in response:
                r['timestamp']  = str(r['timestamp'])
                r['charges']    = json.loads(r['charges']) 
                r['event_info'] = json.loads(r['event_info'])
                output.append(r)
        else:
            output.append({
                "message" : "no event found!!"
            })
        return output[0]