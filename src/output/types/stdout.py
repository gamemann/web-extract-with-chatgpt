import json

from output import OutputBase

class Output(OutputBase):
    def __init__(self, use_json = False, file_path: str = None, file_append = False):
        self.use_json = use_json
        self.file_path = file_path
        self.file_append = file_append
        
    def handle_data(self, url: str, extractor: str, web_data: str, chatgpt_res: str):
        data = f"Web Data Extracted:\n{web_data}"
        
        if chatgpt_res:
            data += f"\n\nReply From ChatGPT:\n{chatgpt_res}"
        
        if self.use_json:
            try:
                obj = {
                    "web_data": web_data
                }
                
                if chatgpt_res:
                    obj["chatgpt_res"] = chatgpt_res
                
                data = json.dumps(obj)
            except Exception as e:
                raise Exception(f"Failed to serialize object: {e}")
            
        print(data)
        
        if self.file_path:
            try:
                mode = 'a' if self.file_append else 'w'
                    
                with open(self.file_path, mode) as f:
                    f.write(data + ('\n' if self.file_append else ''))
            except Exception as e:
                raise Exception(f"Failed to write to file: {e}")