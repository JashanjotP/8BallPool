import Physics
import random
from math import sqrt

def nudge():
    return random.uniform(-1.5, 1.5)

def createTable(table):

    pos = Physics.Coordinate( 
            Physics.TABLE_WIDTH / 2.0,
            Physics.TABLE_WIDTH / 2.0,
                    );
        
    sb = Physics.StillBall(1,pos)

    table+= sb

    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 
                    ,
        Physics.TABLE_WIDTH/2.0 - 
        sqrt(3.0)/1.5*(Physics.BALL_DIAMETER+4.0) 
        
                    );
                
    sb = Physics.StillBall(2,pos)

    table += sb

    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 
     
        ,
        Physics.TABLE_WIDTH/2.0 - 
        sqrt(3.0)/1.5*(Physics.BALL_DIAMETER+4.0) 
        
        );
    sb = Physics.StillBall( 9, pos );
    table += sb;

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+6.0) 
                  
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    2.5*(Physics.BALL_DIAMETER - 4.0) 
                    
                    );
                
    sb = Physics.StillBall(3,pos)

    table += sb

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+6.0) 
                
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    2.5*(Physics.BALL_DIAMETER - 4.0) 
                
                    );
    sb = Physics.StillBall( 10, pos );
    table += sb;

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER - 10.0)/25.0 
                   
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    2.5*(Physics.BALL_DIAMETER - 3.0) 
                   
                    );
    sb = Physics.StillBall( 8, pos );
    table += sb;

    pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER + 4.0)/2.0 
                  
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    3.5*(Physics.BALL_DIAMETER -3.0) 
                    )
    
    sb = Physics.StillBall(7, pos)
    table+= sb

    pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER + 4.0)/2.0 
                   
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    3.5*(Physics.BALL_DIAMETER -3.0) 
                    )
    
    sb = Physics.StillBall(14, pos)
    table+= sb

    pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER + 4.0) * 1.5
              
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    3.5*(Physics.BALL_DIAMETER -3.0) 
                    )
    
    sb = Physics.StillBall(4, pos)
    table+= sb

    pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER + 4.0) * 1.5
                  
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    3.5*(Physics.BALL_DIAMETER -3.0) 
                    )
    
    sb = Physics.StillBall(11, pos)
    table+= sb

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+6.0) 
                   
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    4.5*(Physics.BALL_DIAMETER - 1.5) 
                   
                    );
                
    sb = Physics.StillBall(6,pos)

    table += sb

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+6.0) 
                   
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    4.5*(Physics.BALL_DIAMETER - 1.5) 
                   
                    );
    sb = Physics.StillBall( 15, pos );
    table += sb;

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER - 10.0)/25.0 
                    
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    4.5*(Physics.BALL_DIAMETER - 1.5) 
                    
                    );
    sb = Physics.StillBall( 5, pos );
    table += sb;

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+6.0)*2
                 
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    4.5*(Physics.BALL_DIAMETER - 1.5) 
                   
                    );
                
    sb = Physics.StillBall(12,pos)

    table += sb

    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+6.0) *2
                    ,
                    Physics.TABLE_WIDTH/2.0 - 
                    4.5*(Physics.BALL_DIAMETER - 1.5) 
                    );
    sb = Physics.StillBall( 13, pos );
    table += sb;

    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
    sb  = Physics.StillBall( 0, pos );

    table += sb;

    return table

if __name__ == "__main__":
    table = Physics.Table()
    table = createTable(table)
    with open("setup.svg", "w") as fp:
        fp.write(table.svg())
