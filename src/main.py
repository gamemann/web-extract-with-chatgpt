from sys import exit
from importlib import import_module
from re import sub

from cli import Cli
from config import Config
from chatgpt import ChatGPT
from utils import format

HELP_MENU = """Usage: python3 src/main.py [OPTIONS]

Options:
  -c, --cfg <path>        Path to config file (default: ./conf.json)
  -u, --url <url>         URL to extract web data from. If not specified, you will be prompted at program start.
  -e, --extractor <name>  Extractor to use. If not specified, you will be prompted at program start.
  -l, --list              List settings from the config file and exit.
  -h, --help              Display this help menu and exit.
"""

def main():
    # Parse CLI.
    cli = Cli()
    
    try:
        cli.parse()
    except Exception as e:
        print(f"Failed to parse CLI: {e}")
        
        exit(1)
        
    # Check for help menu.
    if cli.help:
        print(HELP_MENU)
        
        exit(0)
        
    # Parse config.
    cfg = Config()
    
    try:
        cfg.load_from_fs(cli.cfg_path)
    except Exception as e:
        print(f"Failed to load config: {e}")
        
        exit(1)
        
    # Check for list.
    if cli.list:
        cfg.print()
        
        exit(0)
        
    # Check if we should save config to file system.
    if cfg.save_to_fs:
        try:
            cfg.save(cli.cfg_path)
        except Exception as e:
            print(f"Failed to save config to file system: {e}")
            
    # Make sure ChatGPT key exists.
    if not cfg.chatgpt.key:
        print("No ChatGPT API key set. Please modify the config file!")
        
        exit(1)

    # Retrieve URL and extractor to use.
    url = cli.url
    
    if url is None:
        url = input("URL: ").strip()
    else:
        print(f"Using URL: '{url}'...")
    
    extractor_type = cli.extractor
    
    if extractor_type is None:
        extractor_type = input("Extractor [default]: ").strip()
    else:
        print(f"Using Extractor: '{extractor_type}'...")
    
    # Check for default.
    if len(extractor_type) < 1:
        print("Found extractor empty, using 'default'...")
        extractor_type = "default"
        
    # Load extractor class to use.
    try:
        m = import_module(f"extract.extractors.{extractor_type}")
        
        extractor = m.Extractor(
            drv_path = cfg.extract.drv_path,
            agents = cfg.extract.agents
        )
    except Exception as e:
        print(f"Failed to import extractor class: {e}")
        
        exit(1)
        
    # Extract web page content.
    try:
        print("Extracting web data...")
        
        web_data = extractor.extract(url)
        
        # Remove spaces and such often associated with web pages.
        web_data = sub(r'\s+', ' ', web_data).strip()
    except Exception as e:
        print(f"Failed to extract web data: {e}")
        
        exit(1)
    
    # Check if ChatGPT is enabled.
    chatgpt_res: str = None
    
    if cfg.chatgpt.enabled:
        # Create ChatGPT class.
        try:
            print("Initializing ChatGPT client...")
            
            chatgpt = ChatGPT(
                key = cfg.chatgpt.key,
                model = cfg.chatgpt.model,
                max_tokens = cfg.chatgpt.max_tokens,
                temperature = cfg.chatgpt.temperature,
                max_input = cfg.chatgpt.max_input
            )
        except Exception as e:
            print(f"Failed to initialize ChatGPT class: {e}")
            
            exit(1)

        # We need to retrieve role and prompt using the template engine.
        data = {
            "url": url,
            "content": web_data
        }
        
        try:
            role = format(f"{cfg.templates_dir}/{cfg.chatgpt.role_template}.tpl", data)
        except Exception as e:
            print(f"Failed to format ChatGPT role: {e}")
            
            exit(1)
            
        try:
            prompt = format(f"{cfg.templates_dir}/{cfg.chatgpt.prompt_template}.tpl", data)
        except Exception as e:
            print(f"Failed to format ChatGPT prompt: {e}")
            
            exit(1)
            
        # Send ChatGPT request.
        try:
            print("Sending ChatGPT API request...")
            
            chatgpt_res = chatgpt.prompt(role, prompt)
        except Exception as e:
            print(f"Failed to send ChatGPT API request: {e}")
            
            exit(1)
        
    # Initialize output class.
    try:
        type = cfg.output.type
        
        m = import_module(f"output.types.{type}")
        
        to_pass = {}
        
        # Check if we should send data to output class.
        if hasattr(cfg.output, type):
            to_pass = vars(getattr(cfg.output, type))
        
        output = m.Output(**to_pass)
    except Exception as e:
        print(f"Failed to create Output class: {e}")
        
        exit(1)
        
    # Handle output.
    try:
        output.handle_data(url, extractor_type,  web_data, chatgpt_res)
    except Exception as e:
        print(f"Failed to handle output data: {e}")
        
        exit(1)
        
    print("Done! Exiting program...")

    exit(0)
        
if __name__ == "__main__":
    main()