from output import OutputBase

class Output(OutputBase):
    def handle_data(self, url: str, extractor: str, web_data: str, chatgpt_res: str):
        print("Web Data Extracted:")
        print(web_data)
        
        if chatgpt_res:
            print("")
            
            print("Reply From ChatGPT:")
            print(resp)