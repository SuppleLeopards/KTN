import json
import operator


class MessageParser:
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            "msg": self.parse_msg,
            "history": self.parse_hist,
            "names": self.parse_names
            # More key:values pairs are needed
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return None
            # Response not valid


        # [20:00] Server: (Info) content...

    def parse_error(self, payload):
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + "(" + payload["response"] + ") " + payload["content"]

    def parse_info(self, payload):
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + "(" + payload["response"] + ") " + payload["content"]

    def parse_msg(self, payload):
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + "(" + payload["response"] + ") " + payload["content"]

    def parse_hist(self, payload):
        print(payload)
        histlist = []
        for dict in payload:
            histlist.append(dict)
        histlist.sort(key=lambda d: int(d['timestamp']))
        for dict in histlist:
            print(self.parse_msg(dict))

    def parse_names(self, payload):
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + "(" + payload["response"] + ") " + payload["content"]

    def timestamp_convert(self, timestamp):
        return int(timestamp.replace(':', ''))

        # Include more methods for handling the different responses...
