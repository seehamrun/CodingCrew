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

        data = {
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
        self.response.write(template.render(data))



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
        day_log = database.StoredDate(day=dayInput, mood=moodInput, notes=notesInput, sleep=sleepInput, activity=activityInput)
        day_log.put()

class Suggestions(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/suggestions.html')

        self.response.write(template.render())




class ViewDay(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/viewPage.html')

        self.response.write(template.render())




app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/daily_log', EnterInfo),
    ('/suggestions', Suggestions),
    ('/view_day', ViewDay),
], debug=True)
