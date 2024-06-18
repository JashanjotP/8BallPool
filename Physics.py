import phylib;
import sqlite3
import os
from math import sqrt, floor
import random

################################################################################
# import constants from phylib to global varaibles
FRAME_INTERVAL = 0.01
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
HEADER = """
<svg width="325" height="640" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />
""";
FOOTER = """<line x1="0" x2="0" y2="0" y1="0" stroke="black"/>
          </svg>\n""";

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class Hole (phylib.phylib_object):

    #Is the number going to be None or 0.0
    def __init__(self, pos):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0);

        self.__class__ = Hole;

    def svg(self):
        #svg method for the code and giving it the right value
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

class RollingBall (phylib.phylib_object):

    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0);

        self.__class__ = RollingBall;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

    #Add and Svg method later
class HCushion (phylib.phylib_object):

    def __init__(self,y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y);

        self.__class__ = HCushion;

    def svg(self):
        #Check if the cushion is right or left and assigning it the right coordinate
        if self.obj.hcushion.y == 0.0:
            res = -25
        else:
            res = 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (res)

class VCushion (phylib.phylib_object):

    def __init__(self, x):

        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0);

        self.__class__ = VCushion;

    def svg(self):
        #Checking whether the cushion is left or right
        if self.obj.vcushion.x == 0.0:
            res = -25
        else:
            res = 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (res)
        
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):

        str = HEADER;

        #Iterate through the table
        for obj in self:
            #If object exists call svg method and apped to the string
            if obj:
                str += obj.svg()

        str += FOOTER

        return str
    
    def roll( self, t ):

        new = Table();
        
        for ball in self:
            if isinstance( ball, RollingBall ):
        # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
        # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
        # add ball to table
                new += new_ball;
            
            if isinstance( ball, StillBall ):
        # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                            Coordinate( ball.obj.still_ball.pos.x,
                        ball.obj.still_ball.pos.y ) );
        # add ball to table
                new += new_ball;
        # return table
        return new;
    
class Database():

    def __init__(self, reset=False):

        #If reset is true delete the  database file and start fresh
        
        if reset == True:
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')

        #Connect to the database
        Database.conn = sqlite3.connect('phylib.db')
        

    def createDB(self):

        
        cur = Database.conn.cursor()
        
        #Create Tables according to the required description
        cur.execute("""CREATE TABLE IF NOT EXISTS Ball
                                (BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                 BALLNO INTEGER NOT NULL,
                                 XPOS FLOAT NOT NULL,
                                 YPOS FLOAT NOT NULL,
                                 XVEL FLOAT,
                                 YVEL FLOAT);""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TTable
                                 (TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  TIME REAL NOT NULL);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable
                                (BALLID INTEGER NOT NULL,
                                 TABLEID INTEGER NOT NULL,
                                 FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                                 FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID));""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Shot
                                (SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                 PLAYERID INTEGER NOT NULL,
                                 GAMEID INTEGER NOT NULL,
                                 FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                                 FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID));
                        """)
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot
                           (TABLEID INTEGER NOT NULL,
                            SHOTID INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                            FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID));
                        """)
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Game
                          (GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                           GAMENAME VARCHAR(64) NOT NULL);
                        """)
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Player
                          (PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                           GAMEID INTEGER NOT NULL,
                           PLAYERNAME VARCHAR(64) NOT NULL,
                           FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID));
                        """)
        
        #Commit the query and close the cursor
        Database.conn.commit()
        cur.close()
        
        
    def readTable(self, tableID):

        #A new table object
        table = Table()

        cur = Database.conn.cursor()

        idToSearch = tableID + 1

        #See if table exists but better to search tableid in TTable for no balls in the table case
        data = cur.execute("SELECT * FROM BallTable WHERE TABLEID = ?",(idToSearch,))

        exists = data.fetchone()

        if not exists:
            cur.close()
            return None


        #An inner join to get the ball attributs based on the table id
        data = cur.execute("""SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL 
                              FROM BallTable
                              INNER JOIN Ball ON BallTable.BALLID = Ball.BALLID
                            WHERE BallTable.TABLEID = ?;
                        """ ,(idToSearch,))
        
        #Returns an 2d array containing all the balls   
        rows = data.fetchall()
        
        #Adding each row of data into the table class based on if it is a still or rolling
        for row in rows:

            ball_no, xpos, ypos, xvel, yvel = row

            #Still ball have no x and y velocity
            if xvel is None and yvel is None:
                table += StillBall(ball_no, Coordinate(xpos,ypos))

            else:
                #Figuring out the acceleration like in a2
                speed = sqrt((xvel * xvel) + (yvel * yvel))
                
                if speed > VEL_EPSILON:
                    xacc = (-1 * xvel) / speed * DRAG
                    yacc = (-1 * yvel) / speed * DRAG
                    #Adding the rolling ball to the table
                    table += RollingBall(ball_no, Coordinate(xpos,ypos), Coordinate(xvel,yvel), Coordinate(xacc, yacc))


        #Getting 5he time for our table from the db             
        data = cur.execute("""SELECT TIME 
                             FROM TTable
                            WHERE TTable.TABLEID = ?;""", (idToSearch,))
        
        
        timeRow = data.fetchone()
        time = timeRow[0]

        #Adding the time to table
        setattr(table, "time", time)
        

        Database.conn.commit()
        cur.close()
        
        return table
    
    def writeTable(self, table):

        cur = Database.conn.cursor()

        #Inserting the table time into db
        cur.execute("""INSERT
                    INTO TTable (TIME)
                    VALUES (?);
                    """,(table.time,))
        
        #Getting the tableid using the time
        table_id = cur.execute("""SELECT TABLEID FROM TTable WHERE TTable.TIME = ?""",(table.time,))
        table_id = table_id.fetchone()[0]

        #Looping through the table and adding the velocites if it is a rolling else not adding them to our tables
        for obj in table:
            if isinstance(obj, RollingBall):
                cur.execute("""INSERT 
                                INTO   Ball   (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES        (?, ?, ?, ?, ?) """,(obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x
                                                                ,obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x,
                                                                obj.obj.rolling_ball.vel.y))
            elif  isinstance(obj, StillBall):
                cur.execute("""INSERT 
                                INTO   Ball   (BALLNO, XPOS, YPOS)
                                VALUES        (?, ?, ?) """,(obj.obj.still_ball.number, obj.obj.still_ball.pos.x
                                                                ,obj.obj.still_ball.pos.y))
                

            #Adding the ball id and table id so they are related to each other
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                ball_id = cur.execute("SELECT last_insert_rowid()")
                ball_id = ball_id.fetchone()[0]
                cur.execute("""INSERT
                                INTO    BallTable (BALLID, TABLEID)
                                VALUES     (?, ?)""", (ball_id, table_id))

        cur.close()
        Database.conn.commit()

        return table_id - 1
    
    def getGame(self, gameID):

        cur = Database.conn.cursor()

        #Checking if our game exists in the database
        exists = cur.execute("""SELECT * FROM Game WHERE GAMEID = ?;""", (gameID,))
        exists = exists.fetchone()

        if not exists:
            cur.close()
            return [None, None, None]


        #If the game exists doing an inner join to find the name of player names and ids
        data = cur.execute("""SELECT Game.GAMENAME, Player.PLAYERID, Player.PLAYERNAME
                         FROM Player
                        INNER JOIN Game ON Player.GAMEID = Game.GAMEID
                        WHERE Player.GAMEID = ?;
                    """,(gameID,));
        
        #We will have only two rows because 2 players play one game
        row1 = data.fetchone()
        row2 = data.fetchone()

        #Depacking the data
        gameName, row1ID, row1Name = row1
        gameName, row2ID, row2Name = row2

        player1Name, player2Name = None,None

        #Figuring out which player has the lower id and that player becomes player1
        if row1ID < row2ID:
            player1Name = row1Name
            player2Name = row2Name
        else:
            player1Name = row2Name
            player2Name = row1Name

        cur.close()
        Database.conn.commit()

        #Returing the data as an list for easier to depacking
        return [gameName,player1Name,player2Name]
    
    def setGame(self, gameName, player1Name, player2Name):

        cur = Database.conn.cursor()

        #Putting the GameName into table
        cur.execute("""INSERT
                       INTO Game (GAMENAME)
                       VALUES    (?)""", (gameName,))
        
        #Getting the game id
        data = cur.execute("""SELECT GAMEID FROM Game WHERE GAMENAME = ?""" , (gameName,))

        gameID = data.fetchone()[0]

        #Inserting the Player with their name and game id to relate them to each other
        #Player 1 is inserted first
        cur.execute("""INSERT 
                       INTO Player (GAMEID, PLAYERNAME)
                       VALUES      (?, ?)""",(gameID, player1Name))
        
        cur.execute("""INSERT 
                       INTO Player (GAMEID, PLAYERNAME)
                       VALUES      (?, ?)""",(gameID, player2Name))
        
        cur.close()
        Database.conn.commit()
        
    def newShot(self, gameName, playerName):

        cur = Database.conn.cursor()

        #Get the gameid from the gameName
        data = cur.execute("""SELECT GAMEID FROM Game WHERE GAMENAME = ?""", (gameName,))
        gameID = data.fetchone()[0]

        #Get the playerId
        data = cur.execute("""SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?""", (playerName,))
        playerID = data.fetchone()[0]

        #Registering a new shot based on playerid and gameid
        cur.execute("""INSERT
                       INTO Shot (PLAYERID, GAMEID)
                       VALUES    (?, ?)""",(playerID, gameID))
        
        #Getting the shotid
        data = cur.execute("""SELECT SHOTID FROM Shot WHERE PLAYERID = ?""" , (playerID,))

        shot_id = data.fetchone()[0]

        cur.close()
        Database.conn.commit()

        return shot_id - 1
    
    def tableShot(self, shotID, tableID):
        cur = Database.conn.cursor()

        id_table = tableID + 1
        id_shot = shotID + 1

        #Adds the shot to the table in the database relating the shot to the table
        cur.execute("""INSERT
                       INTO TableShot (TABLEID, SHOTID)
                        VALUES        (?, ?)""", (id_table, id_shot))
        
        cur.close()
        Database.conn.commit()
        

    def close(self):
        #Commiting and closing the connection
        Database.conn.commit()
        Database.conn.close()

class Game():

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

        db = Database()
        #Connecting to database

        if isinstance(gameID, int) and not gameName and not player1Name and not player1Name:

            #If only gameid is given and it is an int we get the gamename, playernames from the database
            self.gameId = gameID + 1
            self.gameName, self.player1Name, self.player2Name = db.getGame(self.gameId)

        elif not gameID and isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str):

            #If no gameid but names are given we add a new game to the db
            self.gameName, self.player1Name, self.player2Name = gameName, player1Name, player2Name
            self.gameId = None
            db.setGame(self.gameName, self.player1Name, self.player2Name)
            
        else:
            #If wrong data type is given to constructor
            raise TypeError("Invalid data types passed to Game constructor.")
        
        db.close()

    def shoot(self, gameName, playerName, table, xvel, yvel):

        db = Database()

        #Registering the shot in the database and getting the id
        shot_id = db.newShot(gameName, playerName)


        for obj in table:
            
            #Finding the cue ball in the current table and making it a rolling ball
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                
                obj.type = phylib.PHYLIB_ROLLING_BALL
                obj.obj.rolling_ball.pos.x = obj.obj.still_ball.pos.x
                obj.obj.rolling_ball.pos.y = obj.obj.still_ball.pos.y

                obj.obj.rolling_ball.vel.x = xvel
                obj.obj.rolling_ball.vel.y = yvel

                speed = sqrt((xvel * xvel) + (yvel * yvel))
        
                xacc = (-1 * xvel) / speed * DRAG
                yacc = (-1 * yvel) / speed * DRAG

                obj.obj.rolling_ball.acc.x = xacc
                obj.obj.rolling_ball.acc.y = yacc

                obj.obj.rolling_ball.number = 0

              

        #Now we will figure out the frames for every 10 ms after a shot is played  
        copy = None  
        svgs = []        
        while table:

            #Getting a copy of the table before calling the segment function
            copy = table

            time_start = table.time
            table = table.segment()

            if not table:
                break
            
            time_end = table.time

            #Difference between the start and end time
            time_final =  time_end - time_start

            #Rounding down to the nearest integer
            time_final = int(floor(time_final / FRAME_INTERVAL))

            


            for i in range(time_final):
                #What frame are we one
                time_for_frame = i * FRAME_INTERVAL

                    # Create a new table for the current frame using the roll method
                newtable = copy.roll(time_for_frame)

                    # Set the time of the returned table to the time of the beginning of the segment plus the time for the current frame
                newtable.time = time_start + time_for_frame

                    # Save the table using writeTable to the database
                #table_id = db.writeTable(newtable)

                #Saving the shot to the table to build our animations
                #db.tableShot(shot_id, table_id)

                svgs.append(newtable.svg())

        cueBallfound = False
        eightBallFound = False

        lowBalls = []
        highBalls = []
        for obj in copy:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                cueBallfound = True
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 8:
                eightBallFound = True
            if isinstance(obj, StillBall) and  obj.obj.still_ball.number > 0 and obj.obj.still_ball.number < 8:
                lowBalls.append(obj.obj.still_ball.number)
            if isinstance(obj, StillBall) and obj.obj.still_ball.number > 8:
                highBalls.append(obj.obj.still_ball.number)
        
        if cueBallfound == False:
            copy += StillBall(0, Coordinate(TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                          TABLE_LENGTH - TABLE_WIDTH/2.0))

        

        svgs.append(copy.svg())

        
        
        return [copy, svgs, cueBallfound, eightBallFound, lowBalls, highBalls]
