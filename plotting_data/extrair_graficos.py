import time
from selenium import webdriver
import os 
import shutil


def download_image(image):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '/home/eduardo/Downloads')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/png')        

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("file:///{}".format(image))
    export_button = driver.find_element_by_xpath("//a[@data-title='Download plot as a png']")
    export_button.click()
    time.sleep(10)
    driver.quit()        

def move_rename_image(image_name):
    download_directory = r'/home/eduardo/Downloads'                
    downloaded_file = max([os.path.join(download_directory, f) for f in os.listdir(download_directory)], key=os.path.getmtime)
    print("Arquivo : ", downloaded_file)
    if downloaded_file.endswith('.png'):
        print('Movendo para ', os.path.join(directory, image_name[:-5] + '.png'))
        shutil.move(
            downloaded_file, 
            os.path.join(directory, image_name[:-5] + '.png')
        )   

directory = r'/home/eduardo/UEM/GIT/TCC/data/plot/'
for filename in os.listdir(directory):
    print(directory + filename)
    if filename.endswith(".html"):
        download_image(directory + filename)
        move_rename_image(filename)