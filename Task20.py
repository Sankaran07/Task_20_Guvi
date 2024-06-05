import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains

class Labour_webpage:
    def __init__(self, url):
        self.url = url
        self.download_folder = "D:\shkutty\python\Guvi_task_am"
        self.set_firefox_options()
        self.driver = webdriver.Firefox(options=self.options, service=Service(GeckoDriverManager().install()))

    def set_firefox_options(self):
        self.options = Options()
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", self.download_folder)
        self.options.set_preference("browser.download.useDownloadDir", True)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        self.options.set_preference("pdfjs.disabled",True)

    # Access to given webpage 
    def get_webpage_login(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            sleep(5)
        except Exception as error:
            print("Error on: ", error)

    def create_new_folder(self):
        os.makedirs(self.download_folder, exist_ok=True)

    # Access to get the monthly Report from the webpage 
    def monthly_report(self):
        try:
            document_11 = self.driver.find_element(By.XPATH, '//*[@id="nav"]/li[7]')
            ActionChains(self.driver).move_to_element(document_11).perform()
            sleep(4)
            self.driver.find_element(by=By.XPATH, value='/html/body/nav/div/div/div/ul/li[7]/ul/li[2]/a').click()
            sleep(4)
            self.driver.find_element(by=By.XPATH, value='/html/body/section[3]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/a').click()
            alert = self.driver.switch_to.alert
            alert.accept()
            sleep(4)
        except Exception as error:
            print("Report error message on: ",error)

    # Access & download the images from photo gallery 7th element
    def download_images_webpage(self):
        try:
            self.get_to_International_Labour_Conference()

            # Find image elements with alt attribute "International Labour Conference"
            image_elements = self.driver.find_elements(By.XPATH, '//img[@alt="International Labour Conference"]')

            for img_element in image_elements[:10]:  # Download the 7th, 10 images
                img_url = img_element.get_attribute('src')
                if img_url:
                    img_name = f"image_{image_elements.index(img_element)}.jpg"
                    img_path = os.path.join(self.download_folder, img_name)
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_element.screenshot_as_png)
            print("Images succesfully downloaded")
        except Exception as error:
            print("error message: ",error)
        finally:
            self.driver.quit()

    # Get into the media & photo gallery 
    def get_to_International_Labour_Conference(self):
        try:
            media_page = self.driver.find_element(By.XPATH, '//*[@id="nav"]/li[10]')
            media_page.click()
            sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/div[2]/span/a').click()
        except Exception as error:
            print("gallery error message on: ",error)    
   

url = "https://labour.gov.in/"
la_wp = Labour_webpage(url)
la_wp.create_new_folder()
la_wp.get_webpage_login()
la_wp.monthly_report()
la_wp.download_images_webpage()
