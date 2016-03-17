import json


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
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + payload["content"]

    def parse_hist(self, payload):
        print(self.parse_msg(dict(timestamp="--:--:--", sender="Local", response="Info", content="History")))
        list = payload["content"]
        for dict1 in list:
            print(self.parse_msg(dict1))
        print(self.parse_msg(dict(timestamp="--:--:--", sender="Local", response="Info", content="End of History")))

    def parse_names(self, payload):
        return "[" + payload["timestamp"] + "]" + " " + payload["sender"] + ": " + "(" + payload["response"] + ") " + payload["content"]

        # Include more methods for handling the different responses...