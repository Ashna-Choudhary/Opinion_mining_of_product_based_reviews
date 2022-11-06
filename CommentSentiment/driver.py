import comment_extract as CE
import sentimentYouTube as SYT

from turtle import bgcolor, color
import kivy 
import re
# Import kivy dependencies first
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.screenmanager import ScreenManager, Screen

# Import kivy UX components
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Import other kivy stuff
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.lang import Builder

layout = BoxLayout
black = [0, 0, 0, 0] 
white=[1, 1, 1, 1]
red = [1, 0, 0, 1] 
green = [0, 1, 0, 1] 
blue = [0, 0, 1, 1] 
purple = [1, 0, 1, 1] 

pos =0
neg=0

class LoginPage(layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout components 
        self.vid_id = TextInput(text='Enter Video Id', multiline=False, size_hint=(1,.1))
        self.num_cmt = TextInput(text='Enter number of comments to extract', multiline=False, password=False, size_hint=(1,.1))
        self.button = Button(text="Submit", on_press=self.submit, size_hint=(1,.1), background_color=black, font_size=18)
        self.title_label = Label(text="Video Details", size_hint=(1,.1), font_size=18)

        # Add items to layout
        self.add_widget(self.title_label)
        self.add_widget(self.vid_id)
        self.add_widget(self.num_cmt)
        self.add_widget(self.button)

    def submit(self, *args):
        videoId= str(self.vid_id.text)
        count = int(str(self.num_cmt.text))
        comments = CE.commentExtract(videoId, count)
        alist=SYT.sentiment(comments)
		# Fetch the number of comments
		# if count = -1, fetch all comments
        global pos
        global neg
        pos=str(alist[0])
        neg=str(alist[1])
        cam_app.screen_manager.current='Home'

class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        # Add items to layout
        self.add_widget(Button(text ='Positive sentiment', background_color=blue, on_press=self.change_text))
        self.posi = Label(text=str(pos))
        self.add_widget(self.posi)
        self.add_widget(Button(text ='Negative sentiment',  background_color=red, on_press=self.change_text_neg))
        self.nega = Label(text=str(neg))
        self.add_widget(self.nega)


    def change_text(self, *args):
        self.posi.text = str(pos)

    def change_text_neg(self, *args):
        self.nega.text=str(neg)

class CamApp(App):
    def build(self):

        self.screen_manager = ScreenManager()

        # Info page
        self.login_page = LoginPage()
        screen = Screen(name='Login')
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        self.home_page= HomePage()
        screen = Screen(name='Home')
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    cam_app=CamApp()
    cam_app.run()
