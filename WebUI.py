import tornado.ioloop
import tornado.web

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""<html><body><form action="/" method="post">
                   ID: <input type="text" name="personID">
                   <br/>
                   Num: <input type="text" name="numBuddies">
                   <input type="submit" value="Submit">
                   <br/>
                   </form></body></html>""")

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("Top " + self.get_argument("numBuddies") + " most similar voters for ")
        self.write("ID: " + self.get_argument("personID"))

application = tornado.web.Application([
    (r"/", MyFormHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()