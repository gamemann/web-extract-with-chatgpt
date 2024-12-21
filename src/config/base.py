import json

from utils import safe_write

class Extract():
    def __init__(self):        
        self.drv_path = "/usr/bin/geckodriver"
        self.agents: list[str] = []
        
    def as_dict(self):
        return {
            "drv_path": self.drv_path,
            "agents": self.agents
        }

class ChatGPT():
    def __init__(self):
        self.enabled = True
        self.key: str = None
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
        self.temperature = 0.7
        self.max_input = 500
        self.role_template = "chatgpt_role"
        self.prompt_template = "chatgpt_prompt"
    
    def as_dict(self):
        return {
            "enabled": self.enabled,
            "key": self.key,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "max_input": self.max_input,
            "role_template": self.role_template,
            "prompt_template": self.prompt_template
        }
        
class OutputPost():
    def __init__(self):
        self.url = "http://localhost"
        self.headers: dict[str, str] = {}
        
    def as_dict(self):
        return {
            "url": self.url,
            "headers": self.headers
        }

class Output():
    def __init__(self):
        self.type = "stdout"
        self.post = OutputPost()
        
    def as_dict(self):
        return {
            "type": self.type,
            "post": self.post.as_dict()
        }

class Config():
    def __init__(self):
        self.save_to_fs = False
        
        self.extract = Extract()
        self.chatgpt = ChatGPT()
        self.output = Output()
        
    def as_dict(self):
        return {
            "save_to_fs": self.save_to_fs,
            "extract": self.extract.as_dict(),
            "chatgpt": self.chatgpt.as_dict(),
            "output": self.output.as_dict()   
        }
        
    def load_from_fs(self, path: str):
        data = {}
        
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load JSON data: {e}")
        
        # Get save to filesystem.
        self.save_to_fs = data.get("save_to_fs", self.save_to_fs)
        
        # Get extract config.
        if "extract" in data:
            v = data["extract"]
            
            self.extract.drv_path = v.get("drv_path", self.extract.drv_path)
            
            if "agents" in  v:
                v2 = v["agents"]
                
                for agent in v2:
                    self.extract.agents.append(agent)
        
        # Get ChatGPT config.
        if "chatgpt" in data:
            v = data["chatgpt"]
            
            self.chatgpt.enabled = v.get("enabled", self.chatgpt.enabled)
            self.chatgpt.key = v.get("key", self.chatgpt.key)
            self.chatgpt.model = v.get("model", self.chatgpt.model)
            self.chatgpt.max_tokens = v.get("max_tokens", self.chatgpt.max_tokens)
            self.chatgpt.temperature = v.get("temperature", self.chatgpt.temperature)
            self.chatgpt.max_input = v.get("max_input", self.chatgpt.max_input)
            self.chatgpt.role_template = v.get("role_template", self.chatgpt.role_template)
            self.chatgpt.prompt_template = v.get("prompt_template", self.chatgpt.prompt_template)
            
        # Get output config.
        if "output" in data:
            v = data["output"]
            
            self.output.type = v.get("type", self.output.type)
            
            # Probably a much better way to retrieve the below data, but not a priority at the moment.
            if "post" in v:
                v2 = v["post"]
                
                self.output.post.url = v2.get("url", self.output.post.url)
                
                if "headers" in v2:
                    v3 = v2["headers"]
                    
                    for k, v4 in v3:
                        self.output.post.headers[k] = v4
                        
    def save(self, path: str):
        contents = json.dumps(self.as_dict(), indent = 4)

        safe_write(path, contents)
        
    def print(self):
        # General settings.
        print("General Settings")
        print(f"\tSave To Filesystem => {self.save_to_fs}")
        
        # Extract settings.
        print("Extract Settings")
        print(f"\tDriver Path => {self.extract.drv_path}")
        
        if len(self.extract.agents) > 0:
            print("\tUser Agents")
            
            for v in self.extract.agents:
                print(f"\t\t- {v}")
                
        # ChatGPT Settings.
        print("ChatGPT Settings")
        print(f"\tEnabled => {self.chatgpt.enabled}")
        print(f"\tKey => {self.chatgpt.key}")
        print(f"\tModel => {self.chatgpt.model}")
        print(f"\tMax Tokens => {self.chatgpt.max_tokens}")
        print(f"\tTemperature => {self.chatgpt.temperature}")
        print(f"\tMax Input => {self.chatgpt.max_input}")
        print(f"\tRole Template File => {self.chatgpt.role_template}")
        print(f"\tPrompt Template File => {self.chatgpt.prompt_template}")
        
        # Output settings.
        print("Output Settings")
        print(f"\tType => {self.output.type}")
        print("\tPOST Settings")
        print(f"\t\tURL => {self.output.post.url}")
        
        if len(self.output.post.headers) > 0:
            print("\t\tHeaders")
            
            for k, v in self.output.post.headers.items():
                print(f"\t\t\t{k} => {v}")        