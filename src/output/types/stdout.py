from output import OutputBase

class Output(OutputBase):
    def handle_data(self, url: str, extractor: str, web_data: str, resp: str):
        print("Web Data Extracted:")
        print(web_data)
        
        print("")
        
        print("Reply From ChatGPT:")
        print(resp)