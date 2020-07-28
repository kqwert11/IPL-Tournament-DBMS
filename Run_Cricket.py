import subprocess as sp
import pymysql
import pymysql.cursors

def Report():
    """
    Function to evaluate and analyse the given Database
    """
    print("1. Number of Wins for each team")
    print("2. Best Batsman of the Tournament")
    print("3. Best Bowler of the Tournament")
    print("4. Highest Individual Score of the Tournament (of a Batsman)")
    print("5. Number of Players who are All Rounders, i.e, both Batsman and Bowler")
    print("6. Exit")
    val = int(input("Choose the query you want to execute> "))

    if val == 6:
        return

    elif val == 1:

        try:

            print("")
            print("Number of Wins per Team")
            print("")
            query="SELECT COUNT(M.WonBy) \"COUNT\", T.TeamID FROM MATCHES AS M, TEAMS AS T WHERE WonBy IS NOT NULL AND T.TeamID = M.WonBy GROUP BY T.TeamID"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    elif val == 2:

        try:

            print("")
            print("Best Batsman of the Tournament")
            print("")
            query="SELECT PID, Fname, Lname from PLAYERS WHERE PID = (SELECT PID FROM BATSMAN WHERE Runs = (SELECT MAX(Runs) FROM BATSMAN))"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(str(result[0]['PID'])+": "+result[0]['Fname']+" "+result[0]['Lname'])

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    elif val == 3:

        try:

            print("")
            print("Best Bowler of the Tournament")
            print("")
            query="SELECT PID, Fname, Lname from PLAYERS WHERE PID = (SELECT PID FROM BOWLER WHERE Wickets = (SELECT MAX(Wickets) FROM BOWLER))"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(str(result[0]['PID'])+": "+result[0]['Fname']+" "+result[0]['Lname'])

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    elif val == 4:

        try:

            print("")
            print("Highest Individual Score of the Tournament (of a Batsman)")
            print("")
            query="SELECT PID, Fname, Lname from PLAYERS WHERE PID = (SELECT PID FROM BATSMAN WHERE HighScore = (SELECT MAX(HighScore) FROM BATSMAN))"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(str(result[0]['PID'])+": "+result[0]['Fname']+" "+result[0]['Lname'])

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    elif val == 5:

        try:

            print("")
            print("Number of Players who are All Rounders")
            print("")
            query="SELECT COUNT(*) FROM (SELECT PID, COUNT(PID) FROM PLAYER_TYPE GROUP BY PID HAVING COUNT(PID)=2) A"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print("All Rounders = "+str(result[0]['COUNT(*)']))
            # print("Count = "+str(result[1]['COUNT'])+": "+result[1]['Type'])

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)



def Deletion():
    """
    Function performs the job of Deleting a Venue record if it is demolished
    """
    try:
            
        print("")
        print("________________________________________Deleting a Venue record if it is demolished________________________________________")
        print("")

        print("")
        print("==============================================Enter Venue ID==============================================")
        print("")

        print("VENUE TABLE")
        print("")
        query="SELECT * FROM VENUE"
        print("")
        cur.execute(query)
        result=cur.fetchall()
        print(result)

        print("MATCHES TABLE")
        print("")
        query="SELECT * FROM MATCHES"
        print("")
        cur.execute(query)
        result=cur.fetchall()
        print(result)

        print("")
        vid1 = int(input("Please the Venue ID of the Venue DEMOLISHED: "))
        print("")
        vid2 = int(input("Please the Venue ID where match TO BE HELD: "))
        print("")

        query = "UPDATE MATCHES SET VenueID = '%d' WHERE VenueID = '%d'" %(vid2, vid1)
        cur.execute(query)
        con.commit()

        query = "DELETE FROM VENUE WHERE (VID = '%d')" %(vid1)
        cur.execute(query)
        con.commit()
            
        print("")
        print("==============================================DELETED==============================================")
        print("")

        print("VENUE TABLE")
        print("")
        query="SELECT * FROM VENUE"
        print("")
        cur.execute(query)
        result=cur.fetchall()
        print(result)
            
        print("MATCHES TABLE")
        print("")
        query="SELECT * FROM MATCHES"
        print("")
        cur.execute(query)
        result=cur.fetchall()
        print(result)

    except Exception as e:
        con.rollback()
        print("Failed to update in database")
        print("************",e)
    
    


def Updation():
    """
    Function to update queries mentioned in SRS Document
    """
    print("1. Updating the Records of a Batsman after every match")
    print("2. Updating the Records of a Bowler after every match")
    print("3. Updating the Venue for a Match if due to unforeseen circumstances the match is relocated")
    print("4. Updating the Age of a Player to -1 if he dies due to unforeseen circumstances")
    print("5. Exit")
    val = int(input("Choose the query you want to execute> "))

    if val == 5:
        return

    elif val == 1:
        try:
            print("")
            print("==============================================Enter Any Batsman ID==============================================")
            print("")
            print("BATSMAN TABLE")
            print("")
            query="SELECT * FROM BATSMAN"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

            print("")
            pid = int(input("Please enter the Player ID whose data needs to be updated: "))
            query = "SELECT * FROM BATSMAN WHERE (PID = '%d')" %(pid)
            cur.execute(query)
            result = cur.fetchall() 

            print("")
            inp1 = int(input("Please enter the runs scored by Batsman in the match: "))
            
            op = input("Please if Batsman got Out(Y) or not(N): ")
            print("")
            if op == 'Y':
                inp2 = 0
            else :
                inp2 = 1
            
            query = "UPDATE BATSMAN SET Innings = '%d' WHERE PID = '%d'" %(result[0]['Innings']+1 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BATSMAN SET Runs = '%d' WHERE PID = '%d'" %(result[0]['Runs']+inp1 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BATSMAN SET Innings_Not_Out = '%d' WHERE PID = '%d'" %(result[0]['Innings_Not_Out']+inp2 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BATSMAN SET BatAverage = '%d' WHERE PID = '%d'" %(result[0]['Runs']/(result[0]['Innings']-result[0]['Innings_Not_Out']) , pid)
            cur.execute(query)
            con.commit()

            if result[0]['HighScore'] < inp1:
                query = "UPDATE BATSMAN SET HighScore = '%d' WHERE PID = '%d'" %(inp1, pid)
                cur.execute(query)
                con.commit()   
            
            print("==============================================UPDATED==============================================")

            print("BATSMAN TABLE")
            print("")
            query="SELECT * FROM BATSMAN"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    # +++++++++++++++++++++++++++++++++++++++++++++
    elif val == 2:
        try:
            
            print("")
            print("==============================================Enter Any Bowler ID==============================================")
            print("")

            print("BOWLER TABLE")
            print("")
            query="SELECT * FROM BOWLER"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

            pid = int(input("Please enter the Player ID whose data needs to be updated: "))
            query = "SELECT * FROM BOWLER WHERE (PID = '%d')" %(pid)
            cur.execute(query)
            result = cur.fetchall() 

            print("")
            inp1 = int(input("Please enter the runs given by Bowler in the match: "))
            
            print("")
            inp2 = int(input("Please enter the wickets taken by Bowler in the match: "))
            
            query = "UPDATE BOWLER SET Matches = '%d' WHERE PID = '%d'" %(result[0]['Matches']+1 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BOWLER SET RunsGvn = '%d' WHERE PID = '%d'" %(result[0]['RunsGvn']+inp1 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BOWLER SET Wickets = '%d' WHERE PID = '%d'" %(result[0]['Wickets']+inp2 , pid)
            cur.execute(query)
            con.commit()

            query = "UPDATE BOWLER SET BowlAverage = '%d' WHERE PID = '%d'" %(result[0]['RunsGvn']/result[0]['Matches'] , pid)
            cur.execute(query)
            con.commit()
            
            print("")
            print("==============================================UPDATED==============================================")
            print("")

            print("BOWLER TABLE")
            print("")
            query="SELECT * FROM BOWLER"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)

    # +++++++++++++++++++++++++++++++++++++++++++++
    elif val == 3:
        try:
            
            print("")
            print("==============================================Enter Venue ID and Match ID==============================================")
            print("")

            print("VENUE TABLE")
            print("")
            query="SELECT * FROM VENUE"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

            print("MATCHES TABLE")
            print("")
            query="SELECT * FROM MATCHES"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

            print("")
            tid1 = int(input("Please Enter TeamID 1: "))
            print("")
            tid2 = int(input("Please Enter TeamID 2: "))
            print("")
            day = int(input("Please Day of the Match: "))
            print("")
            vid = int(input("Please the Venue ID where match TO BE HELD: "))
            print("")
            
            query = "UPDATE MATCHES SET VenueID = '%d' WHERE Day = '%d' AND TID1 = '%d' AND TID2 = '%d'" %(vid, day, tid1, tid2)
            cur.execute(query)
            con.commit()

            print("")
            print("==============================================UPDATED==============================================")
            print("")

            print("MATCHES TABLE")
            print("")
            query="SELECT * FROM MATCHES"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)
    
    # +++++++++++++++++++++++++++++++++++++++++++++
    elif val == 4:
        try:
            
            print("")
            print("==============================================Enter Player ID==============================================")
            print("")
            print("PLAYERS TABLE")
            print("")
            query="SELECT * FROM PLAYERS"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

            print("")
            pid = int(input("Please enter the Player ID whose data needs to be updated: "))
            
            death =int(-1)

            query = "UPDATE PLAYERS SET Age = '%d' WHERE PID = '%d'" %(death, pid)
            cur.execute(query)
            con.commit()

            print("")
            print("==============================================UPDATED==============================================")
            print("")

            print("PLAYERS TABLE")
            print("")
            query="SELECT * FROM PLAYERS"
            print("")
            cur.execute(query)
            result=cur.fetchall()
            print(result)

        except Exception as e:
            con.rollback()
            print("Failed to update in database")
            print("************",e)
    
    else:
            print("")
            print("INVALID")






def Insertion():
    ''' 
    Offers all the possible Insertion options into the Database Cricket
    '''
    print("1. Insertion of a New Player into the Team")
    print("2. Insertion of a New Team into the Tournament")
    print("3. Insertion of a New Bowler record if a Batsman starts bowling")
    print("4. Insertion of  a New Batsman record if a Bowler starts batting")
    print("5. Insertion of a New Venue if a new stadium is constructed")
    print("6. Inserting the Man of the Match entry after a match is over")
    print("7. Inserting the Won By entry after the match is over")
    print("8. Exit")

    val = int(input("Enter your choice: "))

    if val == 8:
        return
    
    elif val == 1:
        try:
            print("")
            print("Enter the Player's Details: ")
            player={}
            player["PID"]=int(input("Player ID: "))
            name= input("Name (Fname Lname): ").split(' ')
            player["Fname"] = name[0]
            player["Lname"] = name[1]
            player["Age"] = int(input("Age: "))
            player["JerseyNo"] = int(input("Jersey Number: "))
            player["TeamID"] = int(input("Team ID: "))
            
            query= "SELECT JColour, CaptainID FROM PLAYERS WHERE (TeamID= '%d')"%player["TeamID"]
            cur.execute(query)
            # print(query)
            result=cur.fetchall()

            player["JColour"]=result[0]["JColour"]
            player["CaptainID"]=result[0]["CaptainID"]

            query= "INSERT INTO PLAYERS VALUES('%d', '%s', '%s', '%d', '%d', '%s', '%d', '%d')" %(player["PID"],player["Fname"], player["Lname"], player["Age"],player["JerseyNo"],player["JColour"],player["TeamID"],player["CaptainID"])
            cur.execute(query)

            print("")
            print("Enter the Players Type:")
            print("1. Batsman")
            print("2. Bowler")
            print("3. Both")
            print("")
            value=int(input("Option Selected: "))

            if value == 1:

                query= "INSERT INTO PLAYER_TYPE VALUES('%d', 'Batsman')"%player["PID"]
                cur.execute(query)
                # print(query)
                con.commit()

                batsman={}
                batsman["PID"]=player["PID"]
                batsman["Innings"]=0
                batsman["Innings_Not_Out"]=0
                batsman["Runs"]=0
                batsman["BatAverage"]=0
                batsman["HighScore"]=0

                query="INSERT INTO BATSMAN VALUES('%d', '%d', '%d', '%d', '%d', '%d')"%(batsman["PID"],batsman["Runs"],batsman["Innings"],batsman["Innings_Not_Out"], batsman["BatAverage"], batsman["HighScore"])
                cur.execute(query)
                # print(query)
                con.commit()

                print("")
                print("==============================================INSERTED==============================================")
                print("")


                print("PLAYERS TABLE")
                print("")
                query="SELECT * FROM PLAYERS"
                print("")
                cur.execute(query)
                result=cur.fetchall()
                print(result)

                print("BATSMAN TABLE")
                print("")
                query="SELECT * FROM BATSMAN"
                print("")
                cur.execute(query)
                result=cur.fetchall()
                print(result)
            
            elif value == 2:

                query= "INSERT INTO PLAYER_TYPE VALUES('%d', 'Bowler')"%player["PID"]
                cur.execute(query)
                # print(query)

                con.commit()


                bowler={}
                bowler["PID"]=player["PID"]
                bowler["Matches"]=0
                bowler["RunsGvn"]=0
                bowler["Wickets"]=0
                bowler["BowlAverage"]=0
                bowler["BestFigure"]='0/0'

                query="INSERT INTO BOWLER VALUES('%d', '%d', '%d', '%d', '%d', '%s')"%(bowler["PID"],bowler["Matches"],bowler["RunsGvn"],bowler["Wickets"], bowler["BowlAverage"], bowler["BestFigure"])
                cur.execute(query)
                # print(query)
                con.commit()

                print("")
                print("==============================================INSERTED==============================================")
                print("")


                print("PLAYERS TABLE")
                print("")
                query="SELECT * FROM PLAYERS"
                cur.execute(query)
                result=cur.fetchall()
                print(result)
                print("")

                print("BOWLER TABLE")
                query="SELECT * FROM BOWLER"
                print("")
                cur.execute(query)
                result=cur.fetchall()
                print(result)
                print("")
            
            elif value == 3:

                query= "INSERT INTO PLAYER_TYPE VALUES('%d', 'Batsman')"%player["PID"]
                cur.execute(query)
                # print(query)
                con.commit()

                batsman={}
                batsman["PID"]=player["PID"]
                batsman["Innings"]=0
                batsman["Innings_Not_Out"]=0
                batsman["Runs"]=0
                batsman["BatAverage"]=0
                batsman["HighScore"]=0

                query="INSERT INTO BATSMAN VALUES('%d', '%d', '%d', '%d', '%d', '%d')"%(batsman["PID"],batsman["Runs"],batsman["Innings"],batsman["Innings_Not_Out"], batsman["BatAverage"], batsman["HighScore"])
                cur.execute(query)
                # print(query)
                con.commit()

                query= "INSERT INTO PLAYER_TYPE VALUES('%d', 'Bowler')"%player["PID"]
                cur.execute(query)
                # print(query)
                con.commit()


                bowler={}
                bowler["PID"]=player["PID"]
                bowler["Matches"]=0
                bowler["RunsGvn"]=0
                bowler["Wickets"]=0
                bowler["BowlAverage"]=0
                bowler["BestFigure"]='0/0'

                query="INSERT INTO BOWLER VALUES('%d', '%d', '%d', '%d', '%d', '%s')"%(bowler["PID"],bowler["Matches"],bowler["RunsGvn"],bowler["Wickets"], bowler["BowlAverage"], bowler["BestFigure"])
                cur.execute(query)
                # print(query)
                con.commit()

                print("")
                print("==============================================INSERTED==============================================")
                print("")


                print("PLAYERS TABLE")
                print("")
                query="SELECT * FROM PLAYERS"
                cur.execute(query)
                result=cur.fetchall()
                print(result)
                print("")

                print("BATSMAN TABLE")
                print("")
                query="SELECT * FROM BATSMAN"
                cur.execute(query)
                result=cur.fetchall()
                print(result)
                print("")

                print("BOWLER TABLE")
                print("")
                query="SELECT * FROM BOWLER"
                cur.execute(query)
                result=cur.fetchall()
                print(result)
                print("")

            else:

                print("")
                print("Invalid entry")
                print("")
      
      
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)
        
        return

    elif val == 2:
        try:

            team={}
            print("")
            print("Enter New Team's Details: ")
            team["TeamID"]=int(input("TeamID: "))
            team["Coach"]=input("Coach: ")
            team["CID"]=int(input("Country Code: "))
            team["CName"]=input("Country Name: ")

            query= "INSERT INTO COUNTRY VALUES('%d', '%s')"%(team["CID"], team["CName"])
            cur.execute(query)
            con.commit()
            # print(query)

            query="INSERT INTO TEAMS VALUES('%d', '%s', '%d')"%(team["TeamID"], team["Coach"], team["CID"])
            cur.execute(query)
            con.commit()
            # print(query)

            print("")
            print("==============================================INSERTED==============================================")
            print("")

            print("COUNTRY TABLE")
            print("")
            query="SELECT * FROM COUNTRY"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")

            print("TEAMS TABLE")
            print("")
            query="SELECT * FROM TEAMS"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")


        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)

    elif val == 3:
        try:
            print("")
            pid=int(input("Enter the PID of the Batsman who started Bowling: "))
            print("")

            query="INSERT INTO PLAYER_TYPE VALUES('%d', 'Bowler')"%pid
            cur.execute(query)
            con.commit()
            # print(query)

            query="INSERT INTO BOWLER VALUES('%d', '%d', '%d', '%d', '%d', '%s')"%(pid,0,0,0,0,'0/0')
            cur.execute(query)
            con.commit()
            # print(query)

            print("")
            print("==============================================INSERTED==============================================")
            print("")
            
            print("PLAYER_TYPE TABLE")
            print("")
            query="SELECT * FROM PLAYER_TYPE"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")

            print("BOWLER TABLE")
            print("")
            query="SELECT * FROM BOWLER"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")
        
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)

    elif val == 4:
        try:
            print("")
            pid=int(input("Enter the PID of the Bowler who started Batting: "))
            print("")

            query="INSERT INTO PLAYER_TYPE VALUES('%d', 'Batsman')"%pid
            cur.execute(query)
            con.commit()
            # print(query)

            query="INSERT INTO BATSMAN VALUES('%d', '%d', '%d', '%d', '%d', '%d')"%(pid,0,0,0,0,0)
            cur.execute(query)
            con.commit()
            # print(query)

            print("")
            print("==============================================INSERTED==============================================")
            print("")
            
            print("PLAYER_TYPE TABLE")
            print("")
            query="SELECT * FROM PLAYER_TYPE"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print('')

            print("BATSMAN TABLE")
            print("")
            query="SELECT * FROM BATSMAN"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")
        
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)
    

    elif val == 5:
        try:
            print("")
            print("Enter the details of the newly constructed Venue: ")
            vid=int(input("Venue ID: "))
            venue=input("Venue: ")

            query="INSERT INTO VENUE VALUES('%d', '%s')"%(vid, venue)
            cur.execute(query)
            # print(query)
            con.commit()

            print("")
            print("==============================================INSERTED==============================================")
            print("")
            
            print("VENUE TABLE")
            print("")
            query="SELECT * FROM VENUE"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")
        
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)


    elif val == 6:
        try:
            print("")
            print("Enter the details of the match for which the MoM is to be upated: ")
            tid1=int(input("TeamID 1: "))
            tid2=int(input("TeamID 2: "))
            day=int(input("Day: "))
            mom=int(input("Man of the Match: "))

            query="UPDATE MATCHES SET Man_of_the_Match='%d' WHERE ((TID1='%d' AND TID2='%d' AND Day='%d') OR (TID2='%d' AND TID1='%d' AND Day='%d'))"%(mom,tid1,tid2,day,tid1,tid2,day)
            cur.execute(query)
            # print(query)
            con.commit()

            print("")
            print("==============================================INSERTED==============================================")
            print("")
            
            print("MATCHES TABLE")
            print("")
            query="SELECT * FROM MATCHES"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
            print("")
        
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)
    
    elif val == 7:
        try:
            print("")
            print("Enter the details of the match for which the WonBy is to be upated: ")
            tid1=int(input("TeamID 1: "))
            tid2=int(input("TeamID 2: "))
            day=int(input("Day: "))
            wonby=int(input("WonBy: "))

            query="UPDATE MATCHES SET WonBy='%d' WHERE ((TID1='%d' AND TID2='%d' AND Day='%d') OR (TID2='%d' AND TID1='%d' AND Day='%d'))"%(wonby,tid1,tid2,day,tid1,tid2,day)
            cur.execute(query)
            # print(query)
            con.commit()

            print("")
            print("==============================================INSERTED==============================================")
            print("")
            
            print("MATCHES TABLE")
            query="SELECT * FROM MATCHES"
            cur.execute(query)
            result=cur.fetchall()
            print(result)
        
        except Exception as e:
            con.rollback()
            print("Failed to Insert Into the Database")
            print(">>>>>>>>>>>>>",e)

    else:
        print("")
        print("Error: Invalid Option")
        print("")



        """
        In addition to taking input, you are required to handle domain errors as well

        For example: the SSN should be only 9 characters long
        Sex should be only M or F

        If you choose to take Super_SSN, you need to make sure the foreign key constraint is satisfied

        HINT: Instead of handling all these errors yourself, you can make use of except clause to print the error returned to you by MySQL
        """

        '''query = "INSERT INTO EMPLOYEE(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Dno) VALUES('%s', '%c', '%s', '%s', '%s', '%s', '%c', %f, %d)" %(row["Fname"], row["Minit"], row["Lname"], row["Ssn"], row["Bdate"], row["Address"], row["Sex"], row["Salary"], row["Dno"])

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")'''

    

def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch==1): 
        Insertion()
    elif(ch==2):
        Updation()
    elif(ch==3):
        Deletion()
    elif(ch==4):
        Report()
    else:
        print("Error: Invalid Option")

# Global
while(1):
    tmp = sp.call('clear',shell=True)
    username = input("username: ")
    password = input("password: ")

    try:
        con = pymysql.connect(host='localhost',
                user=username,
                password=password,
                db='CRICKET',
                cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear',shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")
        tmp = input("Enter any key to CONTINUE>")

        with con:
            cur = con.cursor()
            while(1):
                tmp = sp.call('clear',shell=True)
                print("")
                print("======================Functions of Cricket Database======================")
                print("")
                print("1. Insertion")
                print("2. Updation")
                print("3. Delete")
                print("4. Report")
                print("5. Logout")
                print("")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear',shell=True)
                if ch==5:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")


    except:
        tmp = sp.call('clear',shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
    
   

