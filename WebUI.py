import tornado.ioloop
import tornado.web

import MakeAdjacencyMat as util

class MyFormHandler(tornado.web.RequestHandler):
    def writeForm(self):
        self.write("""<html><body><form action="/" method="get">
                   ID: <input type="text" name="personID">
                   <br/>
                   Num: <input type="text" name="numBuddies">
                   <input type="submit" value="Submit">
                   <br/>
                   </form></body></html>""")

    def renderResults(self, personID, numBuddies):
        self.set_header("Content-Type", "text/html")
        self.write("Top " + str(numBuddies) + " most similar voters for ")
        name = util.getName(personID)
        self.write(name)
        self.write(" (ID: " + personID + ")")
        self.write(""" <img width=100 src="http://www.govtrack.us/data/photos/""" +  str(util.getGovID(personID)) + ".jpeg\">")
        self.write(""" <br> """)
        bros = util.getBuddies(personID, numBuddies)
        for friend in bros:
            hyperlink = "/?personID=" + friend + "&numBuddies=" + str(numBuddies)
            self.write("\n<a href='" + hyperlink + "'>" + friend + " : " + util.getName(friend) + "</a>")
            govID = util.getGovID(friend)
            self.write(""" <img width=100 src="http://www.govtrack.us/data/photos/""" +  str(govID) + ".jpeg\">")
            self.write(""" <br> """)

    def get(self):
        util.init()
        numBuddiesStr = self.get_argument("numBuddies", None)
        if numBuddiesStr is not None:
            numBuddies = int(numBuddiesStr)
        else:
            self.writeForm()
            return
        personID = self.get_argument("personID", None)
        if personID is not None:
            self.renderResults(personID, numBuddies)
        else:
            self.writeForm()

application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# H001032
