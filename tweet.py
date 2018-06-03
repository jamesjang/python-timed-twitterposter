####written by scratch by jamesjang 
### explanation of program will be on my website jamesjang.ca

import requests
from requests import cookies, session
from lxml import html
import tkinter
from tkinter import Tk, Label, Button, Entry
from threading import Timer, Thread, Event
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

window = tkinter.Tk()
LOG_URL: 'https://twitter.com/login'
LOGIN_URL: 'https://twitter.com/sessions'
CREATE_URL: 'https://twitter.com/i/tweet/create'
COUNT = 0
scheduler = BackgroundScheduler()

def increment():
    global COUNT
    COUNT = COUNT+1

class AutomatedPosting():  
    def __init__(self,parent):      
        self.user = Label(parent, text="Enter username")
        self.user.pack()
        self.user_entry = Entry(parent)
        self.user_entry.pack()

        self.password = Label(parent, text="Enter password")
        self.password.pack()
        self.pass_entry = Entry(parent, show="*")
        self.pass_entry.pack()

        self.msg = Label(parent, text="Enter Message")
        self.msg.pack()
        self.msg_entry = Entry(parent)
        self.msg_entry.pack()

        self.time = Label(parent, text="Enter Tweet Time in hours (min 1hr.)")
        self.time.pack()
        self.time_entry = Entry(parent)
        self.time_entry.pack()

        self.MyButton = tkinter.Button(window, text="Start")
        self.MyButton.bind("<Button-1>", self.buttonClick)
        self.MyButton.pack()      

    def buttonClick(self, event): 
        startTweet()
        scheduler.start()

AutomatedPosting = AutomatedPosting(window)

def startTweet():
    increment()   
    session = requests.session()
    result = session.get('https://twitter.com/login')
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
    print ('auth token is: ' + authenticity_token)
    payload = {
        'authenticity_token' : {authenticity_token, authenticity_token},
        'redirect_after_login' : '',
        'remember_me' : '1',
        'scribe_log': '',
        'session[password]': AutomatedPosting.pass_entry.get(),
        'session[username_or_email]' : AutomatedPosting.user_entry.get(),
        'ui_metrics':''
    }   
    params ={
        'authenticity_token' : authenticity_token,
        'batch_mode' : 'off',
        'is_permalink_page' :'false',
        'place_id' : '',
        'status' : AutomatedPosting.msg_entry.get() + " " + str(COUNT),
        'tagged_users':''
    }
    result = session.post('https://twitter.com/sessions', data = payload)
    cookies = result.cookies
    result = session.post('https://twitter.com/i/tweet/create', cookies = cookies, params = params, headers =dict(referer = 'https://www.twitter.com/'))
    print(result.text)


scheduler.add_job(startTweet, 'interval', hours=1)

class perpetualTimer():
    def __init__(self, t, hFunction):
        self.t = t  
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

window.mainloop()
