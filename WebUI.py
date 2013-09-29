import tornado.ioloop
import tornado.web
import yaml
import json
from tornado.escape import json_encode
import MakeAdjacencyMat as util

class MyFormHandler(tornado.web.RequestHandler):
    #TODO: Implement
    def ChooseFromList(self, names):
        self.write("Could be any of the following: " + str(names))

    #TODO: Implement
    def NotFound(self, name):
        self.write(name + """: Not Found""")

    def writeForm(self):

        print "this is a tuple: %s" % (util.getVotingRecordTuple("A000055"),)

        self.redirect("static/start.html")
        # self.write("""Name search: <form action="/" method="get">
        #            <input type="text" name="name">
        #            <input type="submit" value="Submit">
        #            </form> <br/>""")
        # self.write("""<html><body><form action="/" method="get">
        #            ID: <input type="text" name="personID">
        #            <br/>
        #            Num: <input type="text" name="numBuddies">
        #            <input type="submit" value="Submit">
        #            <br/>
        #            </form></body></html>""")

    def renderResults(self, personID, numBuddies):
        if numBuddies > 10: # cap number of results displayed
            numBuddies = 10
        count = 1
        self.set_header("Content-Type", "text/html")
        headContent = """
        <html>
        <head>
            <title>TITLE</title>
            <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
             <style>
            .table thead>tr>th, .table tbody>tr>th, .table tfoot>tr>th, .table thead>tr>td, .table tbody>tr>td, .table tfoot>tr>td {
                padding-top:0px;
            }
            </style>
        </head>
        """
        self.write(headContent)
        content1 = unicode("""
        <body>
        <center>
           <img width=100 src="http://www.govtrack.us/data/photos/{curGovID}.jpeg\">
           <br>
           {curName} : {curParty} : {curState}
        """).format(curGovID = util.getGovID(personID),
                   curName  = util.getName(personID).encode('ascii', 'xmlcharrefreplace'),
                   curParty = util.getParty(personID),
                   curState = util.getState(personID))
        self.write(content1)
        bros = util.getBuddies(personID, numBuddies)

        self.write("<table class=\"table\" style = \"width: 750px;\">")
        self.write("<tr>")
        for friendID in bros:
            govID = util.getGovID(friendID)
            self.write("""<td> <img width=100 src="http://www.govtrack.us/data/photos/""" + str(govID) + ".jpeg\">")
        self.write("</tr>")

        self.write("<tr>")
        for friendID in bros:
            self.write("<td>")
            hyperlink = "/?personID=" + friendID + "&numBuddies=" + str(numBuddies)
            self.write("\n<a href='" + hyperlink + "'> " + util.getName(friendID).encode('ascii', 'xmlcharrefreplace') + "</a>")
            self.write("</td>")
        self.write("</tr>")

        self.write("<tr>")
        for friendID in bros:
            self.write("<td>" + util.getParty(friendID) + "</td>")
        self.write("</tr>")

        self.write("<tr>")
        for friendID in bros:
            self.write("<td>" + util.getState(friendID) + "</td>")
        self.write("</tr>")


        self.write("</table>")
        self.write("""Name search: <form action="/" method="get">
                   <input type="text" name="name">
                   <input type="submit" value="Submit">
                   </form>""")
        self.write("</td><td>")
        self.write("</td></tr>")
        self.write("""</center>
                    </body>
                   </html>
                   """)

    def get(self):
        name = self.get_argument("name", None)
        if name is not None:
            personID = util.getIDfromName(name)
            if personID == None:
                self.write(name + """: Not Found""")
                NotFound(self, name)
                return
            #TODO: Maybe change 5 to add feature
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

# Return a json object of the buddies and associated info
# for a given person
class MyBuddiesHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/json")
        personID = self.get_argument("id", None)
        self.write(util.getBuddiesStr(personID))

class VotingRecordHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(range(1, 10)))
        self.finish()

class SearchMemberHandler(tornado.web.RequestHandler):
    def get(self):
        global dataMap
        query = self.get_argument("query", None)

        if len(query) < 3:
            return

        return_dict = dict()
        count = 0
        for k in dataMap:
            if count == 5:
                break
            if query in k["name"]["official_full"].lower():
                return_dict[k["name"]["official_full"]] = dict()
                return_dict[k["name"]["official_full"]]["id"] = k["id"]["govtrack"]
                count += 1
        print json.dumps(return_dict)
        self.write(json_encode(return_dict))

application = tornado.web.Application([
    (r"/", MyFormHandler),
    (r"/personList", MyListHandler),
    (r"/buddiesData", MyBuddiesHandler),
    (r"/ajax", VotingRecordHandler),
    (r"/search", SearchMemberHandler),
], static_path = "static/")

if __name__ == "__main__":
    #f = open('legislators-current.yaml')
    #dataMap = yaml.safe_load(f)
    #f.close()
    util.init()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

