import logging
import re
from dataclasses import dataclass
from tabulate import tabulate
from ktxo.scraper.base_scraper import SeleniumWrapper, By, Keys


log = logging.getLogger("ktxo.myapp")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Scraper data
@dataclass
class Record:
    title:str
    year:int
    stars:str
    sumary:str

#
#
if __name__ == '__main__':
    URL = "https://www.imdb.com/search/title/?genres=comedy"
    log.info(f"Starting browser, url={URL}")
    s = SeleniumWrapper("config.json").start(URL).maximize()
    log.info(f"Started")

    pages= 2
    records: list[Record] = []
    for page in range(pages):
        log.info(f"Getting items from page {page}/{pages}")
        if s.wait_4_presence_of_element_located(By.CSS_SELECTOR, "li[class='ipc-metadata-list-summary-item']"):
            items = s.find_elements(By.CSS_SELECTOR, "li[class='ipc-metadata-list-summary-item']")
        else:
            log.error(f"Cannot locate items, try increasing values for 'wait_ec'")
            break
        for item in items[len(records):]:
            record = Record(
                title=s.find_element(By.TAG_NAME,
                                     "h3",
                                     element=item,
                                     return_text=True,
                                     default=""),
                year=s.find_elements(By.XPATH,
                                     ".//span[contains(@class, 'dli-title-metadata-item')]",
                                     element=item,
                                     return_text=True)[0],
                stars=s.find_element(By.CSS_SELECTOR,
                                     "span[data-testid='ratingGroup--imdb-rating']",
                                     element=item,
                                     return_text=True,
                                     default="").split("\n")[0],
                sumary=s.find_element(By.CSS_SELECTOR,
                                      "div[class='ipc-html-content-inner-div']",
                                      element=item,
                                      return_text=True,
                                      default="")
            )
            record.title = re.sub(r'^[\d\.]+ ', '', record.title).strip()
            records.append(record)

        log.info(f"Page {page} items={len(records)}")
        # Pagination
        s.screenshot()
        s.click_js(By.CSS_SELECTOR,
                   "button[class='ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--on-accent2 ipc-text-button ipc-see-more__button']"
                   )
        log.info(f"Next page")
        s.sleep(5)  # Dummy wait

    print(tabulate([p.__dict__ for p in records], showindex=True))
    s.exit()
