from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command


class GoogleKeywordScreenShooter:
    def __init__(self, keyword, screenshots_dir, max_page):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_page = max_page

    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        for next in range(1, self.max_page + 1):
            try:
                shitty_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g-blk"))
                )
                self.browser.execute_script(
                    """
                const shitty = arguments[0]
                shitty.parentElement.removeChild(shitty)
                """,
                    shitty_element,
                )
            except Exception:
                pass

            search_results = self.browser.find_elements_by_class_name("g")

            for index, search_result in enumerate(search_results):
                search_result.screenshot(
                    f"{self.screenshots_dir}/{self.keyword}x{next}-{index}.png"
                )
            next_page_bar = self.browser.find_element_by_id("pnnext")
            next_page_bar.click()

    def finish(self):
        self.browser.quit()


screen_shoter = GoogleKeywordScreenShooter("python", "screenshots", 4)
screen_shoter.start()
screen_shoter.finish()
