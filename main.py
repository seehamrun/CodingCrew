import webapp2
import jinja2
import os
import database
import logging
import json
import random
import time
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


#HomePageHandler has a get method: Gets the grid template
#          and fills in using loops we will write
class HomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        template = jinja_env.get_template('templates/homepage.html')
        thirty_one = {}
        for i in range(1,32):
            thirty_one[i] = i
        thirty = {}
        for i in range(1,31):
            thirty[i] = i
        february = {}
        for i in range(1,29):
            february[i] = i

        dates = database.StoredDate.query(database.StoredDate.username == user.nickname()).fetch()

        values = {
            'user_nickname': user.nickname(),
            'storedDate':dates,
            'logoutUrl': users.create_logout_url('/'),
            'jan': thirty_one,
            'feb': february,
            'mar': thirty_one,
             'apr': thirty,
             'may': thirty_one,
             'june': thirty,
             'july': thirty_one,
             'aug': thirty_one,
             'sep': thirty,
             'oct': thirty_one,
             'nov': thirty,
             'dec': thirty_one,
        }



        colors = {}
        for date in dates:
            colors[date.day] = date.color

        values["colors"] = colors

        self.response.write(template.render(values))



#EnterInfoHandler has a post method (when the user input box is complete
#and "submit" is hit, this generates a POST request), and a get
#method (template userInoutPage.html of user input boxes)
class EnterInfo(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_env.get_template('templates/userInputPage.html')
        displayDay = self.request.get('day')

        data = {
            'day': displayDay
        }

        storedData = database.StoredDate.query(database.StoredDate.username == user.nickname()).fetch()
        userDates = [storedDatum.day for storedDatum in storedData]

        if(displayDay in userDates):
            self.redirect("/view_day?day=%s" % displayDay)

        self.response.write(template.render(data))

    def post(self):
        user= users.get_current_user().nickname()
        dayInput = self.request.get('day')
        moodInput = self.request.get('mood')
        notesInput = self.request.get('notes')
        sleepInput = self.request.get('sleep')
        activityInput = self.request.get('activity')
# finish if statement for other moods
        colorInput = "white"
        if(moodInput == "happy"):
            colorInput = "#F6D357"
        elif(moodInput == "sad"):
            colorInput="#5687A3"
        elif(moodInput == "angry"):
            colorInput="#CC2431"
        elif(moodInput == "tired"):
            colorInput="#9F9FA1"
        elif(moodInput == "calm"):
            colorInput="#88B24B"
        else:
            colorInput="#2a466d"

        print('received post request')
        print(dayInput + moodInput + notesInput + sleepInput + activityInput)
        day_log = database.StoredDate(day=dayInput, mood=moodInput, notes=notesInput,
                                  sleep=sleepInput, activity=activityInput, color=colorInput, username=user)
        day_log.put()
        time.sleep(0.1)
        self.redirect("/view_day?day=%s" % dayInput)

giphy_api_key = "GgFZf48OO1lfS1C4hm9gMI0jt2sMIaFS"

def queryGiphy(mood):
    url = "http://api.giphy.com/v1/gifs/search?api_key=%s&q=%s&limit=%d"%(giphy_api_key, mood, 100)
    response = json.loads(urlfetch.fetch(url).content)["data"]
    response = random.choice(response)
    response = response["images"]
    response = response["downsized"]
    response = response["url"]
    return response

class Suggestions(webapp2.RequestHandler):
    def get(self):
        user= users.get_current_user().nickname()
        template = jinja_env.get_template('templates/suggestions.html')
        displayDay = self.request.get('day')
        allDays = database.StoredDate.query().fetch()


        queryMood = self.request.get('mood')

        url = 'https://freemusicarchive.org/api/trackSearch?q='+ queryMood +'&limit=50'
        print(urlfetch.fetch(url).content)
        tempResponse = json.loads(urlfetch.fetch(url).content)
        tempResponse = tempResponse["aRows"]
        response = []
        for i in range(0,5):
            response.append(random.choice(tempResponse))



        data = {
            'mood': queryMood,
            'music': response,
            'gif': queryGiphy(queryMood)

        }

        # return self.response.write(queryGiphy(queryMood))

        self.response.write(template.render(data))




class ViewDay(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/viewPage.html')
        displayDay = self.request.get('day')
        allDays = database.StoredDate.query().fetch()
        moodInput = ""
        notesInput = ""
        sleepInput = ""
        activityInput = ""
        for obj in allDays:
            if(obj.day == displayDay):
                moodInput = obj.mood
                notesInput = obj.notes
                sleepInput = obj.sleep
                activityInput = obj.activity
        data = {
            'date': displayDay,
            'mood': moodInput,
            'notes': notesInput,
            'sleep': sleepInput,
            'activity': activityInput
        }
        self.response.write(template.render(data))




app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/daily_log', EnterInfo),
    ('/suggestions', Suggestions),
    ('/view_day', ViewDay),
], debug=True)
