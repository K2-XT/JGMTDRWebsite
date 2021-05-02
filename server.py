from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from urllib.parse import parse_qs
import json
from recipes_db import RecipesDB
from passlib.hash import bcrypt
from session_store import SessionStore

gSessionStore = SessionStore()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def readCookie(self):
        if "Cookie" in self.headers:
            print("The Cookies are:", self.headers["Cookie"])
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    #send any cookie data in self.cookie to the client
    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())
    
    #load the session data for the CURRENT client, using the session ID in self.cookie
    def loadSessionData(self):
        self.readCookie()
        #if session ID is found in the cookie:
        if "sessionID" in self.cookie:
            #load the session ID value from the cookie object
            sessionID = self.cookie["sessionID"].value
            #load the session data from the session store using the session ID
            sessionData = gSessionStore.getSessionData(sessionID)
            #if the session ID is not found in the session store
            if sessionData == None:
                #create a new session and assign a new cookie with the session ID
                sessionID = gSessionStore.createSession()
                sessionData = gSessionStore.getSessionData(sessionID)
                self.cookie["sessionID"] = sessionID
        #otherwise, if no session ID in cookie
        else:
            #create a new session and assign a new cookie with the session ID
            sessionID = gSessionStore.createSession()
            sessionData = gSessionStore.getSessionData(sessionID)
            self.cookie["sessionID"] = sessionID
        self.sessionData = sessionData


    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        self.loadSessionData()
        print("The Path is:", self.path)
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None
        if collection == "recipes":
            if member_id:
                self.handleGetOneRecipe(member_id)
            else:
                self.handleGetRecipes()
        if collection == "users":
            if member_id:
                self.handleGetOneUser(member_id)
            else:
                self.handleNotFound()

    def do_POST(self):
        self.loadSessionData()
        if self.path == "/recipes":
            self.handleCreateRecipe()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleCreateSession()
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.loadSessionData()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


    def do_DELETE(self):
        self.loadSessionData()
        print("The Path is:", self.path)
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None
        if collection == "recipes":
            if member_id:
                self.handleDeleteOneRecipe(member_id)
            else:
                self.handleNotFound()
        if collection == "users":
            if member_id:
                self.handleDeleteOneUser(member_id)
            else:
                self.handleNotFound()
        if collection == "sessions":
            self.handleDeleteSessions();

    def do_PUT(self):
        self.loadSessionData()
        print("The Path is:", self.path)
        parts = self.path.split('/')
        collection = parts[1]
        if len(parts) > 2:
            member_id = parts[2]
        else:
            member_id = None
        if collection == "recipes":
            if member_id:
                self.handleUpdateOneRecipe(member_id)
            else:
                self.handleNotFound()
        if collection == "users":
            if member_id:
                self.handleUpdateOneUser(member_id)
            else:
                self.handleNotFound()

    def handleNotFound(self):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Not Found", "utf-8"))

    def handleForbidden(self):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(bytes("Forbidden", "utf-8"))

    def handle401(self):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(bytes("Not Logged In", "utf-8"))

    def handleUnprocessableEntity(self):
            self.send_response(422)
            self.end_headers()
            self.wfile.write(bytes("Unprocessable Entity", "utf-8"))

#################Get Functions#####################################
    
    def handleGetRecipes(self):
            if "userID" not in self.sessionData:
                self.handle401()
                return
            # 1. Send a status code
            self.send_response(200)
            # 2. Send any headers
            self.send_header("Content-Type", "application/json")
            # 3. Finish headers (whether we have headers or not)
            self.end_headers()
            # 4. Send a body to the client.
            db = RecipesDB()
            allRecipes = db.getAllRecipes()
            self.wfile.write(bytes(json.dumps(allRecipes), "utf-8"))

    def handleGetOneRecipe(self, member_id):
            if "userID" not in self.sessionData:
                self.handle401()
                return
            db = RecipesDB()
            one_recipe = db.getOneRecipe(member_id)
            if one_recipe != None:
                # 1. Send a status code 
                self.send_response(200)
                # 2. Send any headers
                self.send_header("Content-Type", "application/json")
                # 3. Finish headers (whether we have headers or not)
                self.end_headers()
                # 4. Send a body to the client.
                self.wfile.write(bytes(json.dumps(one_recipe), "utf-8"))
            else:
                self.handleNotFound()
    """
    def handleGetOneUser(self, email):
            db = RecipesDB()
            one_user = db.getOneUser(email)
            if one_user != None:
                # 1. Send a status code 
                self.send_response(200)
                # 2. Send any headers
                self.send_header("Content-Type", "application/json")
                # 3. Finish headers (whether we have headers or not)
                self.end_headers()
                # 4. Send a body to the client.
                self.wfile.write(bytes(json.dumps(one_user), "utf-8"))
            else:
                self.handleNotFound()
    """
############################Delete Functions#############################

    def handleDeleteOneRecipe(self, member_id):
            if "userID" not in self.sessionData:
                self.handle401()
                return
            db = RecipesDB()
            one_recipe = db.getOneRecipe(member_id)
            if one_recipe != None:
                db.deleteOneRecipe(member_id)
                # 1. Send a status code
                self.send_response(200)
                # 2. Send any headers
                self.send_header("Content-Type", "application/json")
                # 3. Finish headers (whether we have headers or not)
                self.end_headers()
            else:
                self.handleNotFound()
    """
    def handleDeleteOneUser(self, email):
            db = RecipesDB()
            one_user = db.getOneUser(email)
            if one_user != None:
                db.deleteOneUser(email)
                # 1. Send a status code
                self.send_response(200)
                # 2. Send any headers
                self.send_header("Content-Type", "application/json")
                # 3. Finish headers (whether we have headers or not)
                self.end_headers()
            else:
                self.handleNotFound()
    """
    def handleDeleteSessions(self):
            # Delete the user session
            if 'userID' in self.sessionData:
                del self.sessionData['userID']
                # 1. Send a status code
                self.send_response(200)
                # 2. Send any headers
                self.send_header("Content-Type", "application/json")
                # 3. Finish headers (whether we have headers or not)
                self.end_headers()
            else: 
                self.handleNotFound()

##########################Update Functions#############################

    def handleUpdateOneRecipe(self, member_id):
            if "userID" not in self.sessionData:
                self.handle401()
                return
            db = RecipesDB()
            one_recipe = db.getOneRecipe(member_id)
            if one_recipe != None:
                #1. read the request body
                length = self.headers['Content-length']
                body = self.rfile.read(int(length)).decode("utf-8")
                print("the Body:", body)

                #2. Parse the body into usable data
                parsed_body = parse_qs(body)
                print("parsed BODY:", parsed_body)

                #3. append the new data to our data
                title = parsed_body["title"][0]
                diet = parsed_body["diet"][0]
                ingredients = parsed_body["ingredients"][0]
                instructions = parsed_body["instructions"][0]
                db = RecipesDB()
                db.updateRecipe(title, diet, ingredients, instructions, member_id)

                #4. send a response to the client
                self.send_response(200)
                self.end_headers()
            else:
                self.handleNotFound()

    def handleUpdateOneUser(self, email):
            db = RecipesDB()
            one_user = db.getOneUser(email)
            if one_user != None:
                #1. read the request body
                length = self.headers['Content-length']
                body = self.rfile.read(int(length)).decode("utf-8")
                print("the Body:", body)

                #2. Parse the body into usable data
                parsed_body = parse_qs(body)
                print("parsed BODY:", parsed_body)

                #3. append the new data to our data
                firstName = parsed_body["firstName"][0]
                lastName = parsed_body["lastName"][0]
                email = parsed_body["email"][0]
                db = RecipesDB()
                db.updateUser(firstName, lastName, email)

                #4. send a response to the client
                self.send_response(200)
                self.end_headers()
            else:
                self.handleNotFound()

###################################Create Functions##############################

    def handleCreateRecipe(self):
            if "userID" not in self.sessionData:
                self.handle401()
                return
            #1. read the request body
            length = self.headers['Content-length']
            body = self.rfile.read(int(length)).decode("utf-8")
            print("the Body:", body)

            #2. Parse the body into usable data
            parsed_body = parse_qs(body)
            print("parsed BODY:", parsed_body)

            #3. append the new data to our data
            title = parsed_body["title"][0]
            diet = parsed_body["diet"][0]
            ingredients = parsed_body["ingredients"][0]
            instructions = parsed_body["instructions"][0]
            db = RecipesDB()
            db.insertRecipe(title, diet, ingredients, instructions)

            #4. send a response to the client
            self.send_response(201)
            self.end_headers()

    def handleCreateUser(self):
            #1. read the request body
            length = self.headers['Content-length']
            body = self.rfile.read(int(length)).decode("utf-8")
            print("the Body:", body)

            #2. Parse the body into usable data
            parsed_body = parse_qs(body)
            print("parsed BODY:", parsed_body)

            #3. append the new data to our data
            firstName = parsed_body["firstName"][0]
            lastName = parsed_body["lastName"][0]
            email = parsed_body["email"][0]
            password = parsed_body["password"][0]
            db = RecipesDB()
            if db.getOneUser(email) == None:
                db.insertUser(firstName, lastName, email, password)

                #4. send a response to the client
                self.send_response(201)
                self.end_headers()
            else:
                self.handleUnprocessableEntity()

    def handleCreateSession(self):
            #1. read the request body
            length = self.headers['Content-length']
            body = self.rfile.read(int(length)).decode("utf-8")
            print("the Body:", body)

            #2. Parse the body into usable data
            parsed_body = parse_qs(body)
            print("parsed BODY:", parsed_body)

            #3. append the new data to our data
            email = parsed_body["email"][0]
            password = parsed_body["password"][0]
            db = RecipesDB()
            potentialUser = db.getOneUser(email)
            if potentialUser == None:
                #4. send a response to the client
                self.send_response(401)
                self.end_headers()
            else:
                isMatch = bcrypt.verify(password, potentialUser['password'])
                if isMatch == True:
                    self.send_response(201)
                    self.sessionData['userID'] = potentialUser['id'] 
                    self.end_headers()
                else:
                    self.send_response(401)
                    self.end_headers()
                    
def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyHTTPRequestHandler)
    server.serve_forever()

run()
