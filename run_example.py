from youtube_channel_ripper import YouTube_Channel_Ripper


# here is an example of how to call and use the program yourself. 
if __name__ == '__main__':
    yt = YouTube_Channel_Ripper()
    yt.set_channel_main_url('Enter the channel URL here')
    yt.set_webdriver_location("Enter the path to your Chrome Webdriver here")
    yt.set_save_path('Enter the path to the directory where you want the files to be saved here')
    # next stage is unnessairy, call to change the options of your download.
    yt.download_options('Enter here any specific options your would like, e.g. format="bestaudio"')
    yt.ripper()