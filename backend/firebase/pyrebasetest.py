from logging import exception
from os import kill
import pyrebase
import json
import pprint
from flask import Flask, request

fbconfig = {
    "apiKey": "AIzaSyBRgRRFUlg9XJ6ZrdWxYaoOB5VvQXDaBko",
    "authDomain": "moviematch-c1175.firebaseapp.com",
    "databaseURL": "https://moviematch-c1175-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "moviematch-c1175",
    "storageBucket": "moviematch-c1175.appspot.com",
    "messagingSenderId": "199143205697",
    "appId": "1:199143205697:web:2dbe6c53b964b156ef4fc0",
    "measurementId": "G-8BC59JDXPZ"
  }

pb = pyrebase.initialize_app(fbconfig)
auth = pb.auth()
db = pb.database()





'''
create new User /initial user push
@param userid, email
@returns message
'''
def pushNewUser(userid, email):
    data = {
        "name": "",
        "email": email,
        "groups": "",
        "watchlist": "",
        "antiwatch": "",
        "age": ""
    }

    try:
        print("writing user/ creating user in db")
        db.child("users").set(userid)
        print("Successfully created user in db")

        print("writing user/ writing user data to db")
        db.child("users").child(userid).set(data)
        print("successfully wrote user-data to db")
        return {'message': "User successfully written to db"}, 200
    except Exception as e:
        print("\n" + str(e))
        return {'message': "Error while writing user to db\n" + str(e)}, 400

def setUser(userid,name,email,groups,watchlist,antiwatch,age):
    data = {
        "name" : name,
        "email" : email,
        "groups" : groups,
        "watchlist" : watchlist,
        "antiwatch" : antiwatch,
        "age" : age
    }

    try:
        print("setting user")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully set user")
        return {'message' : "User set"}, 200
    except Exception as e:
        print("\n" + str(e))
        return {'message' : "Error while setting user\n" + str(e)}, 400



'''
updating name to user with localid = userid
@param userid, name
@throws Exception as e
@returns message
'''
def updateName(userid, name):
    data = {
        "name": name
    }
    try:
        print("\nchanging username")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully updated username")

        return {'message': "Username successfully updated"}, 200
    except Exception as e:
        print("\n" + str(e))
        return {'message': "Error while updating username\n" + str(e)}, 400

'''
updating age to user with localid = userid
@param userid, age
@throws Exception as e
@returns message
'''
def updateAge(userid, age):
    data = {
        "age": age
    }

    try:
        print("\nupdating age")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully updated user-age")
        return {'message': "User-Age successfully updated"}, 200
    except Exception as e:
        print("Error:\n " + str(e))
        return {'message': "Error while updating User-Age\n" + str(e)}, 400
        
'''
updateWL with union of existing wl and newwatchlist, which may contain new movies to user with localid = userid
In order to get the existing movies, 'getWatchlist' is executed
@param userid, newwatchlist
@throws Exception as e
@returns message
'''
def updateWatchlist(userid, newwatchlist):
    oldWL = set(getWatchlist(userid))

    if oldWL == newwatchlist:
        print("No new movies watched")
        return {'message' : 'Identical sets - no new movies watched'}

    if "initial item" in oldWL:
        data = {
            "watchlist" : list(newwatchlist)
        }
    else:

        data = {
            "watchlist" : list(oldWL.union(newwatchlist))
            }

    try:
        print("\nupdating wl")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully updated wl")
        return {'message': "wl successfully updated"}, 200
    except Exception as e:
        print("Error:\n " + str(e))
        return {'message': "Error while updating wl\n" + str(e)}, 400


'''
Used to get existing Watchlist of user with localid = userid
@param userid
@returns list(wl)
'''
#returns watchlist as a set
def getWatchlist(userid):
    wl = set()
    
    try:
        tempwl = db.child("users").child(userid).child("watchlist").get()       
        for x in tempwl.each():
            wl.add(x.val())
    except:
         wl.add("initial item")
    return list(wl)



'''
updateAW with union of existing aw and newAntiwatch, which may contain new movies to user with localid = userid
In order to get the existing movies, 'getAntiwatch' is executed
@param userid, newAntiwatch
@throws Exception as e
@returns message
'''
def updateAntiwatch(userid, newAntiwatch):
    oldWL = set(getAntiwatch(userid))

    if oldWL == newAntiwatch:
        print("No new movies watched")
        return {'message' : 'Identical sets - no new movies watched'}

    if "initial item" in oldWL:
        data = {
            "antiwatch" : list(newAntiwatch)
        }
    else:

        data = {
            "antiwatch" : list(oldWL.union(newAntiwatch))
            }

    try:
        print("\nupdating aw")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully updated aw")
        return {'message': "aw successfully updated"}, 200
    except Exception as e:
        print("Error:\n " + str(e))
        return {'message': "Error while updating aw\n" + str(e)}, 400



'''
Used to get existing Antiwatch of user with localid = userid
@param userid
@returns list(aw)
'''
def getAntiwatch(userid):

    aw = set()
    
    try:
        tempaw = db.child("users").child(userid).child("antiwatch").get()       
        for x in tempaw.each():
            aw.add(x.val())
    except:
         aw.add("initial item")
    return list(aw)






'''
Used to get existing groups of user with localid = userid
@param userid
@returns list(gl)
'''
def getGroupList(userid):
    gl = set()
    
    try:
        tempgl = db.child("users").child(userid).child("groups").get()       
        for x in tempgl.each():
            gl.add(x.val())
    except:
         gl.add("initial item")
    return list(gl)

'''
updateGroups with union of existing groups and newGroupList, which may contain new groups to user with localid = userid
In order to get the existing groups, 'getGroupList' is executed
@param userid, newGroupList
@throws Exception as e
@returns message
'''
def updateGroups(userid, newGroupList):
    oldGL = set(getGroupList(userid))
    if oldGL == newGroupList:
        print("No new groups entered")
        return {'message' : 'Identical sets - no new groups entered'}


    if "initial item" in oldGL:
        data = {
            "groups" : list(newGroupList)
        }
    else:

        data = {
            "groups" : list(oldGL.union(newGroupList))
            }

    try:
        print("\nupdating gl")
        db.child("users").child(userid).update(data)
        print("\nSuccessfully updated gl")
        return {'message': "gl successfully updated"}, 200
    except Exception as e:
        print("Error:\n " + str(e))
        return {'message': "Error while updating gl\n" + str(e)}, 400

def getGroupInfo(groupid):
    gi = {}

    try:
        tempgi = db.child("groups").child(groupid).get()
        for x in tempgi.each():
            gi[x.key()] = x.val()
        print(gi)
        return gi
    except Exception as e:
        print("Group does not exist\n" + "Error : " + str(e))
        return{
            'message' : "GroupId does not exist",
            'errorMsg' : str(e)
        }, 400

def initializeNewGroup(name, members, owner):
    if (checkGroupExist(name)):
        try:
            data = {
                "name" : name,
                "members" : members,
                "owner" : owner
            }
            db.child("groups").child(name).set(data)
            print("Group created")

            for m in members:
                try:
                    updateGroups({'user_id' : m, 'GroupList' : [name]})
                except Exception as e:
                    return {
                        'message' : "Error while inserting Group for each member",
                        'error' : str(e)
                    }, 400
        except Exception as e:
            print("Error while creating Group. \n" + "Error : " + str(e))
            return{
                'message' : "Error while creating Group",
                'error' : str(e)
            }, 400

def checkGroupExist(name):
    try:
        data = db.child("groups").child(name).get()
        if (data.val() == None):
            return True
        else: return False
    except:
        return False
'''
name
members
owner
'''

def initializeNewGroup(name, members, owner):
    if (checkGroupExist(name)):
        print("Does not Exist")
        try:
            data = {
                "name" : name,
                "members" : members,
                "owner" : owner
            }

            print("creating group")
            db.child("groups").child(name).set(data)
            print("Group created")

            for m in members:
                try:
                    print("update group for member: " + m)
                    updateGroups(m,[name])
                    print("updated for " + m)
                except Exception as e:
                    return {
                        'message' : "Error while inserting Group for each member",
                        'error' : str(e)
                    }, 400
            print("\n\nsuccessfully updated all members")
        except Exception as e:
            print("Error while creating Group. \n" + "Error : " + str(e))
            return{
                'message' : "Error while creating Group",
                'error' : str(e)
            }, 400
    else:
        print("Group does exist already")
        return {
            'message' : "Group already exists - pls choose another name"
        }


owner = "sJZQk8FH9CU9RBADdXavlssYeP72"

newWl = ["DsxQGGlBiaZ80Fv1WTEemVA6k2j2","sJZQk8FH9CU9RBADdXavlssYeP72"]


data = {
    "name" : "Test for the boys",
    "members" : ["member1", "member2"],
    "owner" : "member1"
}
#db.child("groups").child("123").set(data)

request = {'user_id' : "sJZQk8FH9CU9RBADdXavlssYeP72", 'GroupList' : ["test2"]}

#initializeNewGroup("test2", newWl, owner )
#updateGroups("sJZQk8FH9CU9RBADdXavlssYeP72", ["test2"])


list = getWatchlist("sJZQk8FH9CU9RBADdXavlssYeP72")
pprint.pprint(list)

#getWatchlist("1234")
#pushNewUser("1234", "test@test.com")
#updateWatchlist("1234", newWl)




