import tornado.ioloop
import tornado.web

import MakeAdjacencyMat as util

class MyFormHandler(tornado.web.RequestHandler):
    def NotFound(name):
        self.write(name + """: Not Found""")

    def writeForm(self):
        self.write("""Name search: <form action="/" method="get">
                   <input type="text" name="name">
                   <input type="submit" value="Submit">
                   </form> <br/>""")
        self.write("""<html><body><form action="/" method="get">
                   ID: <input type="text" name="personID">
                   <br/>
                   Num: <input type="text" name="numBuddies">
                   <input type="submit" value="Submit">
                   <br/>
                   </form></body></html>""")

    def renderResults(self, personID, numBuddies):
        count = 1
        self.set_header("Content-Type", "text/html")
        self.write("<center>")
        #elf.write("Top " + str(numBuddies) + " most similar voters for ")
        name = util.getName(personID)
        #elf.write(name)
        #self.write(" (ID: " + personID + ")")
        self.write(""" <img width=100 src="http://www.govtrack.us/data/photos/""" + str(util.getGovID(personID)) + ".jpeg\">")
        self.write(""" <br> """)
        party = util.getParty(personID)
        state = util.getState(personID)
        self.write(name + " : " + party + " : " + state)
        self.write("</center>")
        bros = util.getBuddies(personID, numBuddies)
        self.write("<table border=\"1\">")
        for friendID in bros:
            self.write("<tr>")
            self.write("<td> <b>" + str(count) + ".</b> </td>")
            govID = util.getGovID(friendID)
            self.write("""<td> <img width=100 src="http://www.govtrack.us/data/photos/""" + str(govID) + ".jpeg\">")
            hyperlink = "/?personID=" + friendID + "&numBuddies=" + str(numBuddies)
            self.write("\n<a href='" + hyperlink + "'> " + util.getName(friendID) + "</a>")
            self.write(""" <br> </td> """)
            count += 1
            self.write("<td>" + util.getState(friendID) + "</td>")
            self.write("<td>" + util.getParty(friendID) + "</td>")
            self.write("</tr>")
        self.write("</table>")
        self.write("""Name search: <form action="/" method="get">
                   <input type="text" name="name">
                   <input type="submit" value="Submit">
                   </form>""")

    def get(self):
        name = self.get_argument("name", None)
        if name is not None:
            #TODO: Add feature to see if distance was used
            personID = util.getIDfromName(name)
            if personID == None:
                NotFound(name)
                return
            if (type(personID) == list):
                #TODO: Make page for options
                personID = personID[0]
            self.renderResults(personID, 5)
            return
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

# Return a json list of names of all congress people
class MyListHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/json")
        self.write(util.getPersonListStr())

application = tornado.web.Application([
    (r"/", MyFormHandler),
    (r"/personList", MyListHandler),
], static_path = "static/")

if __name__ == "__main__":
    util.init()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# H001032
