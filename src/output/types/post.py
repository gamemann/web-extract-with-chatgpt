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
        
    def handle_data(self, url: str, extractor: str, web_data: str, resp: str):
        # Create data.
        json = {
            "url": url,
            "extractor": extractor,
            "web_data": web_data,
            "response": resp
        }
        
        post(self.url,
            json = json,
            headers = self.headers
        )