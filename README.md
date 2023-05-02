Youtube Channel Ripper

The youtube channel ripper is a program that allows the user to extract and download all videos off a selected youtube channel. The program runs via a class structure so can be called and directly used in your code. The program requires you have the most upto date selenium Chrome webdriver installed and requires you input the path to its location, as well as the path to the direction you want the files to save to and the URL of the channel.

Before you run the program make sure you install the required moduels in you virtual enviroment. 
  python -m pip install -r requirements.txt
  
Please see the examples.py file for example as to how the program should be called. Ensure you enter the correct url, save path and Selenium Chrome WebDriver path. 

You can specify wither you would like the complete video to be downloaded, or just the audio by calling the download_options() function, see examples.py for how to. 
  for just audio 
    format = 'bestaudio'

UnitTesting of the program can be found in the youtube_ripper_tests.py file. 

Any feedback or bugs noticed can be messaged to me. 

Please enjoy using the program. 
