from output import OutputBase

from requests import post

class Output(OutputBase):
    def __init__(self,
        url: str,
        headers: dict[str, str] = {}    
    ):
        self.url = url
        self.headers = headers
        
        headers["Content-Type"] = "application/json"
        
    def handle_data(self, data: str):
        # Create data.
        json = {
            "response": data
        }
        
        post(self.url,
            json = json,
            headers = self.headers
        )