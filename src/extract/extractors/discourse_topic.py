from extract import ExtractorBase

from bs4 import BeautifulSoup

from selenium.webdriver import Firefox

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Extractor(ExtractorBase):
    def __init__(self,
        drv_path: str = "/usr/bin/geckodriver",
        agents: list[str] = []             
    ):
        super().__init__(
            drv_path = drv_path,
            agents = agents
        )
        
    def wait(self, drv: Firefox):
        # Wait five seconds for 'contents' class is available.
        WebDriverWait(drv, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contents"))
        )
        
    def parse(self, contents: str) -> str:
        # Parse data with BeautifulSoup.
        try:
            soup = BeautifulSoup(contents, "html.parser")
        except Exception as e:
            raise Exception(f"Failed to parse contents with BeautifulSoup: {e}")
        
        # Retrieve text in 'contents' class.
        ele = soup.find("div", class_="regular contents")
        
        if not ele:
            raise Exception(f"Failed to find contents element.")
        
        # Return element text contents.
        return ele.text
    