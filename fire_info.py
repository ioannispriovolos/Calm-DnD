import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("./calmdnd-firebase-adminsdk-5i177-e2b913ce4f.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://calmdnd.firebaseio.com'
})

monsterList = []
def monsterListener(event):

    monster = str(event.data)

    if monster in monsterList:

        monsterList.remove(monster)
        print(monsterList)
    else:

        monsterList.append(monster)
        print(monsterList)

    file = "monsters.txt"

    with open(file, mode = "w") as outfile:
        for s in monsterList:
            if s != 'None':
                outfile.write("%s\n" % s)

firebase_admin.db.reference('/monsters').listen(monsterListener)

attackFromList = []
def attackFromListener(event):

    attackFrom = str(event.data)

    if attackFrom in attackFromList:

        attackFromList.remove(attackFrom)
        print(attackFrom)
    else:

        attackFromList.append(attackFrom)
        print(attackFromList)

    file = "attackFrom.txt"

    with open(file, mode = "w") as outfile:
        for s in attackFromList:
            if s != 'None':
                outfile.write("%s\n" % s)

firebase_admin.db.reference('/attack/from').listen(attackFromListener)

attackToList = []
def attackToListener(event):

    attackTo = str(event.data)

    if attackTo in attackToList:

        attackToList.remove(attackTo)
        print(attackTo)
    else:

        attackToList.append(attackTo)
        print(attackToList)

    file = "attackTo.txt"

    with open(file, mode = "w") as outfile:
        for s in attackToList:
            if s != 'None':
                outfile.write("%s\n" % s)

firebase_admin.db.reference('/attack/to').listen(attackToListener)
