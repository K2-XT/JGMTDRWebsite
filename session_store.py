import base64, os

class SessionStore:
    def __init__(self):
        #dictionary (of dictionaries, one for each client)
        self.sessions = {}

    def generateSessionID(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr


    def createSession(self):
        #Generate a new sessionID
        sessionID = self.generateSessionID()
        #create a new session (dictionary) inside the sessions dictionary
        self.sessions[sessionID] = {}
        #return the new session ID for future access to this session
        return sessionID

    def getSessionData(self, sessionID):
        if sessionID in self.sessions:
            return self.sessions[sessionID]
        return None

    def deleteSession(self):
        #Cleaning Up Stale Sessions
        pass
