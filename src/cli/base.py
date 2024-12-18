from sys import argv

class Cli():
    def __init__(self):
        self.cfg_path = "./conf.json"
        self.list = False
        self.help = False
        
    def parse(self):
        # Parse CLI.
        for k, arg in enumerate(argv):
            # Handle config path.
            if arg.startswith("cfg="):
                self.cfg_path = arg.split('=')[1]
            elif arg == "--cfg" or arg == "-c":
                val_idx = k + 1
                
                if val_idx < len(argv):
                    self.cfg_path = argv[val_idx]
            
            # Handle list.
            if arg == "-l" or arg == "--list":
                self.list = True
                
            # Handle help menu.
            if arg == "-h" or arg == "--help":
                self.help = True