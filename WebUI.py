import tornado.ioloop
import tornado.web

import MakeAdjacencyMat as util

class MyFormHandler(tornado.web.RequestHandler):
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
        self.write(name + " : " + party)
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
            personID = util.getIDfromName(name)
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


application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    util.init()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# H001032
