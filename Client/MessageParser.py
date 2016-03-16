
import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            "msg": self.parse_msg
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return None
            # Response not valid

    def parse_error(self, payload):
        return "Error: " + payload["content"]
    def parse_info(self, payload):
        return "Info: " + payload["content"]
    def parse_msg(self, payload):
        return payload["content"]
    # Include more methods for handling the different responses... 
