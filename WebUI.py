import tornado.ioloop
import tornado.web

import MakeAdjacencyMat as util

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        util.init()
        self.write("""<html><body><form action="/" method="post">
                   ID: <input type="text" name="personID">
                   <br/>
                   Num: <input type="text" name="numBuddies">
                   <input type="submit" value="Submit">
                   <br/>
                   </form></body></html>""")

    def post(self):
        self.set_header("Content-Type", "text/plain")
        numBuddiesStr = self.get_argument("numBuddies")
        numBuddies = int(numBuddiesStr)
        personID = self.get_argument("personID")
        self.write("Top " + numBuddiesStr + " most similar voters for ")
        name = util.getName(personID)
        self.write(name)
        self.write(" (ID: " + personID + ")")
        bros = util.getBuddies(personID, numBuddies)
        for friend in bros:
            self.write("\n" + friend + " : " + util.getName(friend))

application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# H001032