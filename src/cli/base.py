from sys import argv

class Cli():
    def __init__(self):
        self.cfg_path = "./conf.json"
        
        self.url: str = None
        self.extractor: str = None
        
        self.silent = False
        
        self.list = False
        self.help = False
        
    def get_arg_val(self, idx: int, argv: list[str], short_name: str, long_name: str) -> str:
        arg = argv[idx]
        
        if arg.startswith(f"{long_name}="):
            return arg.split("=")[1]
        elif arg == f"--{long_name}" or arg == f"-{short_name}":
            val_idx = idx + 1
            
            if val_idx < len(argv):
                return argv[val_idx]
            
        return None
        
    def parse(self):
        # Parse CLI.
        for k, arg in enumerate(argv):
            # Handle config path.
            v = self.get_arg_val(k, argv, "c", "cfg")
            
            if v:
                self.cfg_path = v
                
            # Handle URL.
            v = self.get_arg_val(k, argv, "u", "url")
            
            if v:
                self.url = v
                
            # Handle extractor.
            v = self.get_arg_val(k, argv, "e", "extractor")
            
            if v:
                self.extractor = v
                
            # Handle silent mode.
            if arg == "-s" or arg == "--silent":
                self.silent = True
            
            # Handle list.
            if arg == "-l" or arg == "--list":
                self.list = True
                
            # Handle help menu.
            if arg == "-h" or arg == "--help":
                self.help = True