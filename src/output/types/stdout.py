from output import OutputBase

class Output(OutputBase):
    def handle_data(self, url: str, extractor: str, web_data: str, resp: str):
        print("Reply from ChatGPT:")
        print(resp)