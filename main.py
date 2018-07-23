import webapp2
import jinja2
import os
from google.appengine.ext import ndb



class DatabaseMoodDays(ndb.Model):
    day = ndb.StringProperty()
    mood = ndb.StringProperty()
    notes = ndb.StringProperty()
    sleep = ndb.IntegerProperty()
    activity = ndb.IntegerProperty()



jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


#HomePageHandler has a get method: Gets the grid template
#          and fills in using loops we will write
class HomePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/homepage.html')
        data = {
             'jan': ""
        }
        self.response.write(template.render(data))



#EnterInfoHandler has a post method (when the user input box is complete
#and "submit" is hit, this generates a POST request), and a get
#method (template userInoutPage.html of user input boxes)
class EnterInfo(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/userInputPage.html')

        self.response.write(template.render())




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
