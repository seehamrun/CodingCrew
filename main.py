import webapp2
import jinja2
import os
import database
from google.appengine.ext import ndb


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


#HomePageHandler has a get method: Gets the grid template
#          and fills in using loops we will write
class HomePage(webapp2.RequestHandler):
    def get(self):
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

        values = {
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

        dates = database.StoredDate.query().fetch()

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
        template = jinja_env.get_template('templates/userInputPage.html')
        displayDay = self.request.get('day')
        data = {
            'day': displayDay
        }
        self.response.write(template.render(data))

    def post(self):
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
                                      sleep=sleepInput, activity=activityInput, color=colorInput)
        day_log.put()
        response_html = jinja_env.get_template('templates/userInputPage.html')
        data = {
            'day': dayInput
        }
        self.response.write(response_html.render(data))

class Suggestions(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/suggestions.html')

        self.response.write(template.render())




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
