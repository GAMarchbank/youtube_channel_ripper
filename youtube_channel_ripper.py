import yt_dlp
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from Errors import WebdriverLocationError, YoutubeChannelSubmenuLocationError, NoChannelURLImputError, NoSavePathSpecifiedError


class YouTube_Channel_Ripper:
    def __init__(self):
        self.vid_number = 0
        self.scraped_url_titles = []
        self.unscraped_videos = []
        self.webdriver_location = None
        self.save_path = None
        self.channel_main_url = None
        self.youtubesubmenuslist = ['VIDEOS', 'SHORTS', 'LIVE']
        self.folder_name = None
        self.sepecific_save_path = None
        self.previous_file_names = []
        self.ydl_opts = None
        self.ydl_opts_edit = False
        self.ext = None
        self.run_test = False
        self.no_download = False
    
    # test_run fuction is called upon in the instance of test. It returns the correct data that can be compared to the test results. 
    def tests_run(self, test = False, no_download = False):
        self.run_test = test
        self.no_download = no_download
        
    # download options gives the user the options to edit how the program acts. Currently it only allows the user to sepecify if they want to download only the audio of the files.
    def download_options(self, format = 'best'):
        if format == 'bestaudio':
            self.ext = '\\%(title)s.mp3'
        else:
            self.ext = '\\%(title)s.%(ext)s'
        self.ydl_opts = {
            'format': format,
            'outtmpl': self.save_path + self.ext,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,  
            'exctract_audio': True   
        }
        self.ydl_opts_edit = True
    
    # a moduel that must be called upon. It allows the user to input what channel they are looking to scrape. 
    def set_channel_main_url(self, channel_main_url):
        self.channel_main_url = channel_main_url
        name_split = self.channel_main_url.split('/')
        for items in name_split:
            try:
                if items[0] == '@':
                    name_confirmed = items
            except IndexError:
                pass
        self.folder_name = name_confirmed.replace('@', '')
        
    # sets the location of the Chrome selenium webdriver. Must be called for the program to work.     
    def set_webdriver_location(self, webdriver_location_path):
        self.webdriver_location = webdriver_location_path
    
    # sets the locaiton of the directory the user wants to save the data into.
    def set_save_path(self, save_path):
        self.save_path = save_path
    
    # function that checks if a directory for the channel already exists. If it does it extracts the titles of the files in that directory into a list to be compared with the videos being downloaded. 
    def folder_check_and_create(self):
        if self.save_path == None:
            raise NoSavePathSpecifiedError('No save path has been specified. Please specify save path.')
        if self.run_test == True and self.no_download == False:
            self.save_path = self.save_path + '\\' + 'test'
            if os.path.exists(self.save_path) == False:
                os.mkdir(self.save_path)
        self.sepecific_save_path = self.save_path + '\\' + self.folder_name
        if os.path.exists(self.sepecific_save_path) == False:
            if self.no_download == False:
                os.mkdir(self.sepecific_save_path)
        else:
            files = os.listdir(self.sepecific_save_path)
            for file_names in files:
                try:
                    ext_name = file_names.split('.')
                    name = file_names.replace(ext_name[-1], '')
                    self.previous_file_names.append(name)
                except Exception:
                    pass
        self.ydl_opts['outtmpl'] = self.sepecific_save_path + self.ext
    
    # loads an instance of selenium for the rest of the program to use.
    def selenium_load(self, url):
        chromeOptions = Options()
        if self.run_test == False:
            chromeOptions.headless = True
        else:
            chromeOptions.headless = False
        chromeOptions.add_argument('--mute-audio')
        try:
            driver = webdriver.Chrome(executable_path = self.webdriver_location, options=chromeOptions)
        except Exception:
            raise WebdriverLocationError('You need to call set_webdriver_location to imput a Selenium Chrome WebDriver Path.')
        driver.get(url)
        time.sleep(2)
        return driver
    
    # navigates out of the accept cookies pop up that appears on youtube each time a new selenium instance is loaded. 
    def cookie_page_navigation(self, driver):
        cookie_button = driver.find_element(By.CSS_SELECTOR,'c-wiz')
        cookie_button = cookie_button.find_element(By.CLASS_NAME,'kFwPee')
        cookie_button = cookie_button.find_element(By.CLASS_NAME,'NIoIEf')
        cookie_button = cookie_button.find_element(By.CLASS_NAME,'G4njw')
        cookie_button = cookie_button.find_element(By.CLASS_NAME, 'qqtRac')
        cookie_button = cookie_button.find_element(By.CLASS_NAME, 'VtwTSb')
        cookie_button = cookie_button.find_elements(By.CSS_SELECTOR, 'form')
        cookie_button = cookie_button[1]
        cookie_button.click()
        time.sleep(2)
        return driver
    
    # returns a list of elements that each represent a single video on the channel.
    def return_urls_and_video_titles(self, driver):
        video_locator = driver.find_element(By.ID, 'content')
        video_locator = video_locator.find_element(By.CSS_SELECTOR, 'ytd-two-column-browse-results-renderer')
        video_locator = video_locator.find_element(By.CSS_SELECTOR, 'ytd-rich-grid-renderer')
        video_locator = video_locator.find_element(By.ID, 'contents')
        videos = video_locator.find_elements(By.CSS_SELECTOR, 'ytd-rich-item-renderer')
        return videos

    # scrolls down to the bottom of the page. Ensures that the program scrapes all videos for the subcategories on a channels page. 
    def scroll_down_page(self, driver, first_call = True, shorts = False):
        if first_call == True:
            self.vid_number = 0
        videos_num = len(self.return_urls_and_video_titles(driver))
        scroll_check = True
        while True:
            htmlelement = driver.find_element(By.TAG_NAME, 'html')
            htmlelement.send_keys(Keys.END)
            time.sleep(1)
            new_videos_num = len(self.return_urls_and_video_titles(driver))
            if new_videos_num == videos_num:
                scroll_check = False
            if scroll_check == False:
                break
            videos_num = new_videos_num
        videos_lst = self.return_urls_and_video_titles(driver)
        while self.vid_number != videos_num:
            try:
                title = videos_lst[self.vid_number].find_element(By.ID, 'dismissible')
                title = title.find_element(By.ID, 'details')
                if shorts == True:
                    title = title.find_element(By.CLASS_NAME, 'yt-simple-endpoint')
                else:
                    title = title.find_element(By.ID, 'meta')
                    title = title.find_element(By.ID, 'video-title-link')
                title_name = title.get_attribute('title')
                title_url = title.get_attribute('href')
            except Exception as e:
                return False
            else:
                print(f'video {self.vid_number+1}/{videos_num} accessed.')
                if title_url not in self.previous_file_names and self.no_download != True:
                    try:
                        videos_lst[self.vid_number].click()
                    except Exception:
                        return False
                    else:
                        time.sleep(2)
                        try:
                            with yt_dlp.YoutubeDL(self.ydl_opts)as ydl:
                                video = ydl.extract_info(driver.current_url, download = True)
                                name = video.get('title', None)
                            connection_check = True
                        except Exception:
                            connection_check = False
                        else:
                            print(name + ' has been successfully downloaded.')
                        driver.execute_script("window.history.go(-1)")
                        if connection_check == False:
                            self.unscraped_videos.append({'title': title_name, 'url': title_url})
                        self.vid_number += 1
                else:
                    self.vid_number += 1    
        if self.run_test == True:
            return videos_lst
        else:
            return 'Pass'
    
    # navigates between different submenus that appear on a channels page to search for the menu that is imput as the argument section. If no corrent page is found the program returns False.
    def navigate_to_channel_section(self, driver, section):
        video_page = driver.find_element(By.ID, 'content')
        video_page = video_page.find_element(By.ID, 'page-manager')
        video_page = video_page.find_element(By.ID, 'header')
        video_page = video_page.find_element(By.ID, 'tabsContainer')
        buttons = video_page.find_elements(By.CSS_SELECTOR, 'tp-yt-paper-tab')
        for elements in buttons: 
            text = elements.find_element(By.CSS_SELECTOR, 'div')
            text = elements.find_element(By.CLASS_NAME, 'tab-title')
            try: 
                texts = text.text
                if texts == section:
                    text.click()
                    time.sleep(2)
                    return driver
            except Exception:
                try:
                    raise YoutubeChannelSubmenuLocationError(f'Browser is unable to locate the {section} Submenu.')
                except YoutubeChannelSubmenuLocationError as e:
                    print(e)
        return False
    
    # Main funciton of the program. When called upon and as long as set up correctly the program will begin scraping the data off the input youtube channel.
    def ripper(self):
        if self.ydl_opts_edit == False:
            self.download_options()
        self.folder_check_and_create()
        if self.run_test == True:
            test_videos_lst = []
        for submenus in self.youtubesubmenuslist:
            if submenus == 'SHORTS':
                shorts = True
            else:
                shorts = False
            returned_videos = True
            while True:
                try:
                    driver.quit()
                except Exception:
                    pass
                try:
                    driver = self.selenium_load(self.channel_main_url)
                except Exception:
                    raise NoChannelURLImputError('No url or an invalid URL has been input into the program. Please set a valid URL.')
                self.cookie_page_navigation(driver)
                driver_navigation_check = self.navigate_to_channel_section(driver, submenus)
                if driver_navigation_check != False:
                    if returned_videos == True:
                        returned_videos = self.scroll_down_page(driver, True, shorts)
                    elif returned_videos == False:
                        returned_videos = self.scroll_down_page(driver, False, shorts)
                    if returned_videos != False:
                        if self.run_test == True:
                            test_videos_lst = test_videos_lst + returned_videos
                        break
                else:
                    break
            driver.quit()
        print('Program ended.')
        if self.run_test == True:
            if self.no_download == True:
                return test_videos_lst
            else:
                return self.sepecific_save_path

                