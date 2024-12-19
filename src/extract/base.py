from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

from selenium.webdriver.remote.command import Command

from random import choice

class ExtractorBase():
    def __init__(self,
        drv_path: str = "/usr/bin/geckodriver",
        agents: list[str] = []             
    ):
        self.drv_path = drv_path
        self.agents = agents
        
    def create_driver(self) -> Firefox:
        # Setup options.
        opts = Options()
        
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        
        # Pick random user agent if any.
        if len(self.agents) > 0:
            # Get random user agent.
            ua = choice(self.agents)
            
            opts.set_preference("general.useragent.override", ua)
    
        service = Service(executable_path = self.drv_path)
        
        return Firefox(options = opts, service = service)
    
    def close_driver(self, drv: Firefox):
        drv.close()
        
    def wait(self, drv: Firefox):
        pass
        
    def parse(self, contents: str) -> str:
        pass
        
    def extract(self, url: str) -> str:
        # Create driver.
        try:
            drv = self.create_driver()
        except Exception as e:
            raise Exception(f"Failed to create Firefox driver: {e}")
        
        # Load web page.
        try:
            drv.get(url)
        except Exception as e:
            raise Exception(f"Failed to parse web page: {e}")
        
        # Wait for web page to be ready.
        try:
            self.wait(drv)
        except Exception as e:
            raise Exception(f"Failed to wait for web page: {e}")
        
        # Parse web page.
        try:
            ret = self.parse(drv.page_source)
        except Exception as e:
            raise Exception(f"Failed to parse web page: {e}")
        
        # Close driver and return result.
        try:
            self.close_driver(drv)
        except Exception as e:
            raise Exception(f"Failed to close web driver: {e}")
        
        return ret