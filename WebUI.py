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
        self.redirect("static/start.html")
        # self.write("""Name search: <form action="/" method="get">
        #            <input type="text" name="name">
        #            <input type="submit" >""")
        # self.write("""<html><body><form action="/" method="get">
        #            ID: <input type="text" name="personID">
        #            <br/>
        #            Num: <input type="text" name="numBuddies">
        #            <input type="submit" value="Submit">
        #            <br/>
        #            </form></body></html>""")

    def renderResults(self, personID, numBuddies):
        global state_info

        if numBuddies > 10: # cap number of results displayed
            numBuddies = 10
        count = 1
        self.set_header("Content-Type", "text/html")
        headContent = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Congress Buddies</title>

            <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
            <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
            <link rel="stylesheet" type="text/css" href="/static/css/jquery-ui-modified.css">
            <link href="/static/styles.css" rel="stylesheet" type="text/css" />
            <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
             <style>
            .table thead>tr>th, .table tbody>tr>th, .table tfoot>tr>th, .table thead>tr>td, .table tbody>tr>td, .table tfoot>tr>td {
                padding-top:0px;
            }
            </style>
        </head>
        <body>

        <div id = "top_bar">
            <a href="#" id="bottle" onclick='window.location = "/"';return false;" >
                <img style="" class = "bar_logo" src="static/capitol13.png">
            </a>
            <input placeholder = "Search by State or Representative Name"id="top_search" type="text" />
            <img style="" class = "search_img" src="static/search.png">
        </div>

        <script>
test = ""
$(document).ready(function () {
    $("#top_search").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://localhost:8080/search",
                data: {
                    query: request.term,
                    pagesize: 10
                },
                jsonp: "jsonp",
                dataType: "jsonp",
                error: function(jqXHR, textStatus) {
                  //alert( "Request failed: " + textStatus );
                },
                complete: function (xhr, status) {
                if (status === 'error' || !xhr.responseText) {
                    //alert("error");
                  }
                  else {
                      var data = JSON.parse(xhr.responseText);

                      var realArray = $.makeArray( data )
                      response($.map( data, function(val, key) {
                        // Do something
                        console.log(val);
                        console.log(key);
                        return {
                            value: key,
                            avatar: "http://www.govtrack.us/data/photos/" + val["id"] + ".jpeg"
                        };

                      }));

                      /*
                      for(var full_name in data){
                        console.log(full_name);
                        console.log(data[full_name]["id"]);
                      }
                     */

                  }
                },
                success: function(data) {
                    response($.map(data.users, function(el, index) {
                        return {
                            value: el.display_name,
                            avatar: "http://www.govtrack.us/data/photos/{" +  + "curGovID}.jpeg"
                        };
                    }));
                }
            });
        }
    }).data("uiAutocomplete")._renderItem = function (ul, item) {
        return $("<li />")
            .data("item.autocomplete", item)
            .append("<a><img class = 'search_autocomplete_image' src='" + item.avatar + "' />" + "<span class = \'search_autocomplete_name\'>" + item.value + "</span></a>")
            .appendTo(ul);
    };

  $( "#top_search" ).autocomplete({ autoFocus: true });

    $("#top_search").keydown(function(e){
      if (e.keyCode === 13){
       if(document.getElementById("ui-id-1").childNodes.length != 0) {
          window.location = "/?name=" + $("#top_search").val();
        }
      }
    });
});
</script>

<style type="text/css">
  .search_autocomplete_image {
   padding-right: 10px;
   max-width: 48px;
   padding-top: 8px;
  }
  .ui-autocomplete > li {
    height: 72px;
    font: 24px "Helvetica-Light","Lucida Grande", Helvetica, Arial, sans-serif;
  }
  .search_autocomplete_name {
    position: absolute;
    padding-top: 15px;
  }
</style>


        <script>
            var map_color = new Object();
            map_color["Republican"] = [];
            map_color["Democrat"] = [];

        </script>

       """
        self.write(headContent)
        bros = util.getBuddies(personID, numBuddies)

        self.write("""<div class="container" style="margin-top: 40px; max-width: 270px; height:80px;">""");
        self.write("<table class=\"table\">")
        self.write("<tr>")
        self.write("<td style=\"border: none;\">")
        self.write("""<div class = "img_holder">""")
        self.write("<img width=70 src=\"http://www.govtrack.us/data/photos/" + str(util.getGovID(personID)) + ".jpeg\">")
        self.write("</div>")
        self.write("<span class = \"primary_name\">" + util.getName(personID).encode('ascii', 'xmlcharrefreplace') + "</span>")
        self.write("<span class = \"result_party\">" + util.getParty(personID) + "</span>")
        self.write("<span class = \"result_state\">" + state_info[util.getState(personID)]["name"] + "</span>")
        self.write("</td>")
        self.write("</tr>")
        self.write("</table>")
        self.write("</div>");

        self.write("<script>")


        self.write("map_item = {};")
        self.write("map_item['name'] = \"" + util.getName(personID) + "\";")
        self.write("map_item['state'] = \"" + util.getState(personID) + "\";")
        self.write("map_item['district'] = \"" + str(util.getDistrict(personID)) + "\";")

        if str(util.getParty(personID)) == "Republican":
            if util.getDistrict(personID) != "":
                if int(util.getDistrict(personID)) < 10:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + "0" + str(util.getDistrict(personID)) + ";")
                    self.write("map_color[\"Republican\"].push(map_item);")
                else:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + str(util.getDistrict(personID)) + ";")
                    self.write("map_color[\"Republican\"].push(map_item);")
            else:
                self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + str(util.getDistrict(personID)) + ";")
                self.write("map_color[\"Republican\"].push(map_item);")
        elif str(util.getParty(personID)) == "Democrat":
            if util.getDistrict(personID) != "":
                if int(util.getDistrict(personID)) < 10:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + "0" + str(util.getDistrict(personID)) + ";")
                    self.write("map_color[\"Democrat\"].push(map_item);")
                else:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + str(util.getDistrict(personID)) + ";")
                    self.write("map_color[\"Democrat\"].push(map_item);")
            else:
                self.write("map_item[\"code\"] = " + str(state_info[util.getState(personID)]["code"]) + str(util.getDistrict(personID)) + ";")
                self.write("map_color[\"Democrat\"].push(map_item);")
        self.write("</script>")
        self.write("<tr>")


        self.write("""<div class="container" style="margin-top: 30px; max-width: 1300px;">""");
        self.write("<table class=\"table\">")

        count = 0;
        for friendID in bros:
            count+=1
            if count == 1:
                continue


            self.write("<script>")

            self.write("map_item = {};")
            self.write("map_item['name'] = \"" + util.getName(friendID[0]) + "\";")
            self.write("map_item['state'] = \"" + util.getState(friendID[0]) + "\";")
            self.write("map_item['district'] = \"" + str(util.getDistrict(friendID[0])) + "\";")

            if str(util.getParty(friendID[0])) == "Republican":
                if util.getDistrict(friendID[0]) != "":
                    if int(util.getDistrict(friendID[0])) < 10:
                        self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + "0" + str(util.getDistrict(friendID[0])) + ";")
                        self.write("map_color[\"Republican\"].push(map_item);")
                    else:
                        self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + str(util.getDistrict(friendID[0])) + ";")
                        self.write("map_color[\"Republican\"].push(map_item);")
                else:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + str(util.getDistrict(friendID[0])) + ";")
                    self.write("map_color[\"Republican\"].push(map_item);")
            elif str(util.getParty(friendID[0])) == "Democrat":
                if util.getDistrict(friendID[0]) != "":
                    if int(util.getDistrict(friendID[0])) < 10:
                        self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + "0" + str(util.getDistrict(friendID[0])) + ";")
                        self.write("map_color[\"Democrat\"].push(map_item);")
                    else:
                        self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + str(util.getDistrict(friendID[0])) + ";")
                        self.write("map_color[\"Democrat\"].push(map_item);")
                else:
                    self.write("map_item[\"code\"] = " + str(state_info[util.getState(friendID[0])]["code"]) + str(util.getDistrict(friendID[0])) + ";")
                    self.write("map_color[\"Democrat\"].push(map_item);")

            self.write("</script>")
            self.write("<tr>")

            govID = util.getGovID(friendID[0])
            self.write("<td style=\"border: none;\">")
	    self.write("<div class = \"blue_bar\" style=\"width 280px;\">Loading</div>")
            self.write("""<div class = "img_holder"><img width=70 src="http://www.govtrack.us/data/photos/""" + str(govID) + ".jpeg\"></div>")
            hyperlink = "/?personID=" + friendID[0] + "&numBuddies=" + str(numBuddies)
            self.write("\n<a class = \"result_url\" href='" + hyperlink + "'> " + util.getName(friendID[0]).encode('ascii', 'xmlcharrefreplace') + "</a>")
            self.write("<span class = \"result_party\">" + util.getParty(friendID[0]) + "</span>")
            self.write("<span class = \"result_state\">" + state_info[util.getState(friendID[0])]["name"] + "</span>")
            self.write("</td>")
            self.write("</tr>")
        self.write("</table>")

        self.write("""
        <img src = "static/load.gif" id = "loading" style="margin-left: 600px;top: -300px;position: relative;"></img>
        <div id = "chart"></div>
        <script src="http://d3js.org/d3.v3.min.js"></script>
        <script src="http://d3js.org/queue.v1.min.js"></script>
        <script src="http://d3js.org/topojson.v1.min.js"></script>
        <script src="http://d3js.org/topojson.v1.min.js"></script>
        <script src="/static/js/map.js"></script>""")

        self.write("</div>");

        self.write("</td><td>")
        self.write("</td></tr>")
        self.write("""</center>
        <div id="footer" style="
    /* height: 100px; */opacity: 0;
">
      <div class="container" style="
    height: 100px;
">
        <br>
        <br>
        <p style="text-align: center;"><span class="" style="
    font: 20px &quot;Helvetica-Light&quot;,&quot;Lucida Grande&quot;, Helvetica, Arial, sans-serif;
    color: rgba(123,134,151,1);
">Congress Buddies</span></p>
        <p class="text-muted credit" style="text-align: center;">See who votes like who in congress</p>
        <p class="text-muted credit" style="text-align: center;">Anil Ganti, Saurabh Davala, Neal Bhasin, Vijay Thurimella</p>
      	<p class="text-muted credit" style="text-align: center;">Voting Records from <a href="http://www.govtrack.us/">GovTrack.us</a>
        Map from <a href="http://bl.ocks.org/mbostock">mbostock</a> View Code <a href="https://github.com/thisisneal/CongressBuddies">GitHub</a></p>

      </div>
    </div>
</body>
</html>
                   """)

    def decode_argument(self, value, name):
        return value.decode('latin-1')

    def get(self):
        name = self.get_argument("name", None)
        if name is not None:
            personID = util.getIDfromName(name)
            if personID == None:
                self.write(name + """: Not Found""")
                #NotFound(self, name)
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
        global state_info
        query = self.get_argument("query", None)

        print "\ngot query: "
        print query

        if len(query) < 3:
            return

        return_dict = dict()
        count = 0
        for k in dataMap:
            if count == 5:
                break
            if query.lower() in k["name"]["official_full"].lower():
                return_dict[k["name"]["official_full"]] = dict()
                return_dict[k["name"]["official_full"]]["id"] = k["id"]["govtrack"]
                count += 1
            elif query.lower() in state_info[k['terms'][-1]['state']]['name'].lower():
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
    f = open('legislators-current.yaml')
    dataMap = yaml.safe_load(f)
    f.close()

    #Parse us-state-names.tsv
    #ex. CA
        #code: 6
        #name: California

    state_info ={}
    with open("static/js/us-state-names.tsv") as f:
        for line in f:
            (code,state_id,name) =  line.split(None,2)
            state_info[state_id]= {}
            state_info[state_id]["code"] = code
            state_info[state_id]["name"] = name

    util.init()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

