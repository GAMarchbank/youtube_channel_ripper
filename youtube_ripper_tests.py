import unittest
from youtube_channel_ripper import YouTube_Channel_Ripper
from selenium.webdriver.common.by import By
import os


class YoutubeRipperTests(unittest.TestCase):
    # set up conditions for the start of each test.
    def setUp(self):
        self.ripper = YouTube_Channel_Ripper()
        self.main_url = 'Test url of channel to be scraped'
        self.ripper.set_webdriver_location("Path of selenium Chrome webdriver")
        self.ripper.set_save_path('Path of direction test program will save files into. Files are deleted at the end of the test.')        
        self.ripper.set_channel_main_url(self.main_url)
        self.ripper.download_options(format='bestaudio')
        self.driver = self.ripper.selenium_load(self.main_url)
        
    # testing wither the driver has sucessfully navigated away from the accept cookies popup.
    def test_cookie_navigation(self):
        cookieless = self.ripper.cookie_page_navigation(self.driver)
        self.assertEqual(cookieless.current_url, self.main_url, 'The page has unsuccessfuly navigated the cookies popup and not moved onto the correct page.')
        
    # tests that the program correctly navigates to each submenus page. The test only runs if that page exists on the site. 
    def test_video_page_navigation(self):
        self.ripper.cookie_page_navigation(self.driver)
        for items in ['VIDEOS', 'SHORTS', 'LIVE']:
            check = self.ripper.navigate_to_channel_section(self.driver, items)
            if check != False:
                if items == 'LIVE':
                    url_append_check = '/streams'
                else:
                    url_append_check ='/' + items.lower()
                self.assertEqual(self.driver.current_url, self.main_url + url_append_check, 'The program has not managed to move onto the video page of the youtube channel.')
                self.driver.execute_script('window.history.go(-1)')
    
    # test to see if the program has located the correct number of videos that appear on the channels page. 
    def test_program_locates_all_videos(self):
        self.ripper.cookie_page_navigation(self.driver)
        video_page = self.driver.find_element(By.ID, 'content')
        video_page = video_page.find_element(By.ID, 'page-manager')
        video_page = video_page.find_element(By.ID, 'header')
        video_page = video_page.find_element(By.ID, 'channel-container')
        video_page = video_page.find_element(By.ID, 'inner-header-container')
        video_page = video_page.find_element(By.ID, 'videos-count')
        video_count = video_page.find_elements(By.CSS_SELECTOR, 'span')
        for items in video_count:
            text = items.text
            try:
                text = int(text)
            except ValueError:
                pass
            else:
                number_of_videos = text
        self.driver.quit()
        self.ripper.tests_run(test=True, no_download=True)
        test = self.ripper.ripper()
        self.assertEqual(len(test), number_of_videos, 'The test has not scraped the correct number of videos.')
    
    # test to see that every video on the channels page have been sucessfully downloaded. The downloaded files are deleted at the end of the test.
    def test_all_files_download(self):
        self.ripper.cookie_page_navigation(self.driver)
        video_page = self.driver.find_element(By.ID, 'content')
        video_page = video_page.find_element(By.ID, 'page-manager')
        video_page = video_page.find_element(By.ID, 'header')
        video_page = video_page.find_element(By.ID, 'channel-container')
        video_page = video_page.find_element(By.ID, 'inner-header-container')
        video_page = video_page.find_element(By.ID, 'videos-count')
        video_count = video_page.find_elements(By.CSS_SELECTOR, 'span')
        for items in video_count:
            text = items.text
            try:
                text = int(text)
            except ValueError:
                pass
            else:
                number_of_videos = text
        self.driver.quit()
        self.ripper.tests_run(test=True)
        out_save_path = self.ripper.ripper()
        files = os.listdir(out_save_path)
        self.assertEqual(len(files), number_of_videos, 'The correct number of videos have not been downloaded.')
        del_save_path = out_save_path.split('\\')
        print(del_save_path)
        del_save_path = out_save_path.replace(del_save_path[-1], '')
        for items in files:
            temp_save_path = out_save_path + '\\' + items
            os.remove(temp_save_path)
        os.rmdir(out_save_path)
        os.rmdir(del_save_path)
        
    # the tear down requirments after each test is run. 
    def tearDown(self):
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()