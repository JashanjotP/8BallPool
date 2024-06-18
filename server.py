import sys
import cgi
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import Physics
from set import createTable
import json
import random


class MyHandler(BaseHTTPRequestHandler):
    
    table = None
    player1_name = None
    player2_name = None
    game_name = None
    game = None
    currentPlayer = None
    highBalls = []
    lowBalls = []
    cueBallFound = None
    eightBallFound = None
    assignedBalls = False
    player1Assigned = None
    player2Assigned = None

    player1Balls = []
    player2Balls = []

    playerWon = None

    def do_GET(self):

        #Parse the url
        parsed = urlparse(self.path)

        if parsed.path == '/':
            fp = open("./index.html")
            content = fp.read()
            MyHandler.table = None
            MyHandler.player1_name = None
            MyHandler.player2_name = None
            MyHandler.game_name = None
            MyHandler.game = None
            MyHandler.currentPlayer = None
            MyHandler.highBalls = []
            MyHandler.lowBalls = []
            MyHandler.cueBallFound = None
            MyHandler.eightBallFound = None
            MyHandler.assignedBalls = False
            MyHandler.player1Assigned = None
            MyHandler.player2Assigned = None

            MyHandler.player1Balls = []
            MyHandler.player2Balls = []

            MyHandler.playerWon = None

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length" , len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

            fp.close()

        #If the path is a table
        elif parsed.path in ["/script.js"]:
            fp = open("./script.js")
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/js")
            self.send_header("Content-length" , len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

            fp.close()

        elif parsed.path in ["/info"]:
            
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "applications/json" );
            self.end_headers();
        
            data = [MyHandler.currentPlayer, MyHandler.player1Assigned, MyHandler.player2Assigned, MyHandler.playerWon, MyHandler.player1Balls, MyHandler.player2Balls]

            data_json = json.dumps(data)

            self.wfile.write(bytes(data_json,"utf8"));
        
        elif parsed.path in ["/update"]:
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "applications/json" );
            self.end_headers();
        
            data = MyHandler.table.svg()

            data_json = json.dumps(data)

            self.wfile.write(bytes(data_json,"utf8"));

        elif parsed.path in ["/styles.css"]:
            fp = open("./styles.css")
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length" , len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

            fp.close()

        elif parsed.path in ["/index.css"]:
            fp = open("./index.css")
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length" , len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

            fp.close()

        elif parsed.path.startswith('/table'):

            #try catch to see if file exits else send a 404 response 
            try:
                #Try seeing if the file exists and send that back to the server
                fp = open("."+parsed.path, 'rb')
                content = fp.read()

                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                self.send_header("Content-length", len(content))
                self.end_headers()

                self.wfile.write(content)
                fp.close()

            except FileNotFoundError:
                #Send 404 if file does not exist
                print("File not Found")
                self.send_response( 404 );
                self.end_headers();
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):

        parsed = urlparse(self.path)

        if parsed.path in ['/game.html']:

            #Getting the form data
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } )
            
            #Removes all the svg files
            for file in os.listdir('.'):
                if file.startswith("table-") and file.endswith(".svg"):
                    os.remove(file)

            #Store the form data into variables
            MyHandler.player1_name = str(form.getvalue("player1_name"))
            MyHandler.player2_name = str(form.getvalue("player2_name"))
            MyHandler.game_name = str(form.getvalue("game_name"))

            MyHandler.currentPlayer = random.randrange(0, 1)

            self.db = Physics.Database(reset=True)
            self.db.createDB()

            MyHandler.game = Physics.Game(gameName= MyHandler.game_name,player1Name= MyHandler.player1_name,player2Name=MyHandler.player2_name)

            MyHandler.table = Physics.Table()

            MyHandler.table = createTable(MyHandler.table)

            MyHandler.currentPlayer = random.randint(0,1)

            player1Nameattr, player2Nameattr, player1pictureattr, player2pictureattr = "uncurrent-1", "uncurrent-2","",""

            if MyHandler.currentPlayer == 0:
                player1Nameattr = "current-1"
                player2pictureattr = "passive"
            else:
                player2Nameattr = "current-2"
                player1pictureattr = "passive"


            page = """ <!DOCTYPE html>
                        <html lang="en">
                        <head>
	                        <meta charset="UTF-8">
	                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	                        <title>8 Ball Pool</title>
                            <link href='https://fonts.googleapis.com/css?family=Krona One' rel='stylesheet'>
                            <link rel="preconnect" href="https://fonts.googleapis.com">
                            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                            <link href="https://fonts.googleapis.com/css2?family=Kadwa:wght@400;700&display=swap" rel="stylesheet">
                            <link rel="stylesheet" href="styles.css"/>
                        </head>
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js">
                        </script>
                        <script src="script.js"></script>
                        <body>
                        <div class="con">
                          <div class = "player-con">
	                        <div class="names %s" id="player1-name-select">
	                            <p>%s</p>
	                            </div>
	                            <div>
		                            <h1 class="balls-title">Balls To Pot:</h1>
		                            <div class="balls-con" id="player-1-hORl"></div>

                                    <div class="img-con %s" id="player1-image">
                                        <img width="220" height="241" src="https://www.emoji.co.uk/files/google-emojis/activity-android/8306-billiards.png" alt="Current Player Image">
                                    </div>
                                </div>
                            </div>
                          <div>
                        """%(player1Nameattr, MyHandler.player1_name, player1pictureattr)
            
            page += MyHandler.table.svg()
            

            page += """
                           </div>
                           <div class="player-con">
                        <div class="names %s" id="player2-name-select">
                        <p class="player2-name">%s</p>

                        </div>
                        <div>
                            <h1 class="balls-title">Balls To Pot:</h1>
                            <div class="balls-con" id="player-2-hORl"></div>

                            <div class="img-con %s" id="player2-image">
                                <img width="220" height="241" src="https://www.emoji.co.uk/files/google-emojis/activity-android/8306-billiards.png" alt="Current Player Image">
                            </div>
                        </div>
                        </div>

                        </div>
                        <div class="win-con passive" >
                            <div class="win-form">
                                <h1 class="win-title">Congratulations!!!</h1>
                                <p class="win-name">Sehaj</p>
                                <p class="win-desc">You're the champion of the table!</p>
                                <div class="new-con">
                                    <form action="/" method="get">
                                        <input type="submit" value="New Game" class="new-game-btn">
                                    </form>
                                </div>
                            </div>
                        </div>
                        </body>
                        </html>
                        """ % (player2Nameattr, MyHandler.player2_name, player2pictureattr)

            


            
            #Sending a 200 response and sending the dynamic HTML String
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( page ) );
            self.end_headers();
        
            self.wfile.write(bytes(page,"utf8"));
        

        elif parsed.path in ['/data.html']:
            
            for file in os.listdir('.'):
                if file.startswith("table") and file.endswith(".svg"):
                    os.remove(file)
            content_len = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_len).decode('utf-8')
            data = json.loads(post_data)

            svgs= []

            MyHandler.table, svgs, MyHandler.cueBallFound,MyHandler.eightBallFound, MyHandler.lowBalls, MyHandler.highBalls= MyHandler.game.shoot(MyHandler.game_name,MyHandler.player1_name,MyHandler.table, -1 * float( data["velx"]),-1 * float( data["vely"]))

            if MyHandler.eightBallFound == False:

                if MyHandler.player1Assigned == "High":
                    MyHandler.player1Balls = MyHandler.highBalls
                    MyHandler.player2Balls = MyHandler.lowBalls
                else:
                    MyHandler.player1Balls = MyHandler.lowBalls
                    MyHandler.player2Balls =  MyHandler.highBalls

                if MyHandler.currentPlayer == 0:
                    
                    if len(MyHandler.player1Balls) == 0:
                        MyHandler.playerWon = MyHandler.player1_name
                    else:
                        MyHandler.playerWon = MyHandler.player2_name
                else:

                    if len(MyHandler.player2Balls) == 0:
                        MyHandler.playerWon = MyHandler.player2_name
                    else:
                        MyHandler.playerWon = MyHandler.player1_name


            if MyHandler.assignedBalls == False:
                if len(MyHandler.highBalls) == 7 and len(MyHandler.lowBalls) == 7:
                    MyHandler.player1Assigned = None
                    MyHandler.player2Assigned = None
                    
                    if MyHandler.currentPlayer == 0:
                        MyHandler.currentPlayer = 1
                    else:
                        MyHandler.currentPlayer = 0
                
                elif MyHandler.currentPlayer == 0:
                    if len(MyHandler.highBalls) > len(MyHandler.lowBalls):
                        MyHandler.player1Assigned = "Low"
                        MyHandler.player1Balls = MyHandler.lowBalls

                        MyHandler.player2Assigned = "High"
                        MyHandler.player2Balls =  MyHandler.highBalls
                    elif len(MyHandler.highBalls) < len(MyHandler.lowBalls):
                        MyHandler.player1Assigned = "High"
                        MyHandler.player1Balls = MyHandler.highBalls

                        MyHandler.player2Assigned = "Low"
                        MyHandler.player2Balls =  MyHandler.lowBalls
                    else:
                        MyHandler.player1Assigned = "High"
                        MyHandler.player1Balls = MyHandler.highBalls

                        MyHandler.player2Assigned = "Low"
                        MyHandler.player2Balls =  MyHandler.lowBalls
                    
                    MyHandler.assignedBalls = True
                    MyHandler.currentPlayer = 0

                elif MyHandler.currentPlayer == 1:
                    if len(MyHandler.highBalls) > len(MyHandler.lowBalls):
                        MyHandler.player2Assigned = "Low"
                        MyHandler.player2Balls = MyHandler.lowBalls
                        MyHandler.player1Assigned = "High"
                        MyHandler.player1Balls = MyHandler.highBalls
                    elif len(MyHandler.highBalls) < len(MyHandler.lowBalls):
                        MyHandler.player2Assigned = "High"
                        MyHandler.player2Balls = MyHandler.highBalls
                        MyHandler.player1Assigned = "Low"
                        MyHandler.player1Balls = MyHandler.lowBalls
                    else:
                        MyHandler.player1Assigned = "Low"
                        MyHandler.player1Balls = MyHandler.lowBalls
                        MyHandler.player2Assigned = "High"
                        MyHandler.player2Balls = MyHandler.highBalls
                    
                    MyHandler.assignedBalls = True
                    MyHandler.currentPlayer = 1

            else:
                if MyHandler.currentPlayer == 0:
                    if MyHandler.player1Assigned == "High":
                        if len(MyHandler.highBalls) == len(MyHandler.player1Balls):
                            MyHandler.currentPlayer = 1
                            MyHandler.player2Balls = MyHandler.lowBalls
                        else:
                            MyHandler.player1Balls = MyHandler.highBalls
                            MyHandler.player2Balls = MyHandler.lowBalls
                    else:
                        if len(MyHandler.lowBalls) == len(MyHandler.player1Balls):
                            MyHandler.currentPlayer = 1
                            MyHandler.player2Balls = MyHandler.highBalls
                        else:
                            MyHandler.player1Balls = MyHandler.lowBalls
                            MyHandler.player2Balls = MyHandler.highBalls

                else:
                    if MyHandler.player2Assigned == "High":
                        if len(MyHandler.highBalls) == len(MyHandler.player2Balls):
                            MyHandler.currentPlayer = 0
                            MyHandler.player1Balls = MyHandler.lowBalls
                        else:
                            MyHandler.player2Balls = MyHandler.highBalls
                            MyHandler.player1Balls = MyHandler.lowBalls
                    else:
                        if len(MyHandler.lowBalls) == len(MyHandler.player2Balls):
                            MyHandler.currentPlayer = 0
                            MyHandler.player1Balls = MyHandler.highBalls
                        else:
                            MyHandler.player1Balls = MyHandler.highBalls
                            MyHandler.player2Balls = MyHandler.lowBalls
            
            
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "applications/json" );
            self.end_headers();

            svgs_json = json.dumps(svgs)
        
            self.wfile.write(bytes(svgs_json,"utf8"));

            

        else:
            #If the endpoint does not exist send 404
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );




if __name__ == "__main__":
    #Get the port from command line and then start the server
    port = int(sys.argv[1] )
    httpd = HTTPServer( ( 'localhost', port), MyHandler );
    print( "Server listing in port: "+ str(port) );
    httpd.serve_forever();