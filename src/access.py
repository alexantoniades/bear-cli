import requests
import json
import os
import pyotp
import bcrypt
import re
import time

class HiddenPassword(object):
    def __init__(self, password=''):
        self.password = password
    def __str__(self):
        return '*' * len(self.password)

class User:
    def __init__(self, email, password, otp_secret, api_key=str(), fingerprint=str(), base_url="qgg.hud.ac.uk"):
        self.email = email
        self.__password = password
        self.__otp_secret = otp_secret
        self.__fingerprint = fingerprint
        self.__api_key = api_key
        self.base_url = base_url

        self.session = requests.Session()
    
        self.isLoggedIn = False
        self.login_response = self.verifyLogin(self.login())

    @property
    def fingerprint(self):
        return(self.__fingerprint)

    @property
    def password(self):
        return(self.__password)

    @property
    def tfa(self):
        return(pyotp.TOTP(self.__otp_secret).now())

    @property
    def api_key(self):
        return(self.__api_key)

    @staticmethod
    def jsonResponse(response):
        return(json.loads(re.match("\{(.*?)\}", response.text).group(0)))


    def verifyLogin(self, login):
        response = self.jsonResponse(login)
        if response['error'] is True:
            if response['message'] == 'Invalid Authentication Code':
                login = self.verifyLogin(self.login())
        else:
            self.isLoggedIn = True
        return(login)


    def login(self):
        try:
            login_response = self.session.post(
                url=f"https://{self.base_url}/access/login.php", 
                headers={ 
                    'User-Agent': 'Mozilla/5.0'
                }, 
                data={
                    'email': self.email,
                    'password': self.password,
                    'tfaCode': self.tfa,
                    'fp': self.fingerprint
                }
            )
            return(login_response)
            

        except Exception as error:
            print(error)

    def logout(self):
        pass

    def getIP(self):
        pass

    def getAPI(self, action=str(), data=dict()):
        params = { 'a': action, **data }
        headers = { 'API_KEY': self.api_key }
        api_response = self.session.get(
            url=f"https://{self.base_url}/controller/api.php", 
            headers=headers,
            params=params
        )
        return(api_response)


class Admin(User):
    def __init__(self, email, password, otp_secret, api_key=str(), fingerprint=str()):
        super().__init__(email, password, otp_secret, api_key=api_key, fingerprint=fingerprint)

#-----------------------------------------[ Utility ]---------------------------------------------#

    @property
    def blockedAttempts(self):
        return(self.getAPI('blockedAttempts').text)

    @property
    def sessionsCount(self):
        return(self.getAPI('sessionsCount').text)

    @property
    def listActivity(self):
        return(self.getAPI('listActivity').text)

    def failsCount(self):
        return(self.getAPI('failsCount').text)

    def loadConfig(self):
        return(self.getAPI('loadConfig').text)

    def saveConfig(self):
        return(self.getAPI('saveConfig').text)

    def sendTGMessage(self):
        return(self.getAPI('sentTGMessage').text)

    def viewLoginAttempts(self):
        return(self.getAPI('viewLoginAttempts').text)

    def requestsLogs(self):
        return(self.getAPI('requestsLogs').text)

#-----------------------------------------[ Groups ]---------------------------------------------#
    def createGroup(self):
        return(self.getAPI('createGroup').text)

    def listGroups(self):
        return(self.getAPI('listGroups').text)

    def deleteGroup(self):
        return(self.getAPI('deleteGroup').text)
#-----------------------------------------[ Users ]---------------------------------------------#
    def toggleUserActive(self):
        return(self.getAPI('toggleUserActive').text)

    def syncUsers(self):
        return(self.getAPI('syncUsers').text)

    def onlineUsersCount(self):
        return(self.getAPI('onlineUserCount').text)


    def userBehaviour(self):
        return(self.getAPI('userBehaviour').text)


    def listUsers(self):
        return(self.getAPI('listUsers').text)


    def listDistinctIPs(self):
        return(self.getAPI('listDistinctIPs').text)

    def deleteUser(self):
        return(self.getAPI('deleteUser').text)

    def sessionsGeo(self):
        return(self.getAPI('sessionsGeo').text)

    def viewUserBrowserRecords(self, user):
        return(self.getAPI('viewUserBrowserRecords', data={ 'u': user }).text)

    def viewUserActivity(self, user):
        return(self.getAPI('viewUserActivity', data={ 'u': user }).text)

    def viewUserLoginRecords(self):
        return(self.getAPI('viewUserLoginRecords').text)

    def viewUser(self, user):
        return(self.getAPI('viewUser', data={ 'u': user }).text)

#-----------------------------------------[ System ]---------------------------------------------#
    def systemUserExists(self):
        return(self.getAPI('systemUserExists').text)

    def createSystemUser(self):
        return(self.getAPI('createSystemUser').text)

    def removeSystemUser(self):
        return(self.getAPI('removeSystemUser').text)

    def listServers(self):
        return(self.getAPI('listServers').text)



# user = User('email@email.com', 'password123', '669452')
# test = user.login()

"""
API actions = [
"blockedAttempts",
"userBehaviour","listActivity","listUsers","listDistinctIPs","deleteUser","toggleUserActive","listGroups","createGroup","deleteGroup",
"sessionsCount","onlineUsersCount","failsCount","sessionsGeo","viewUserBrowserRecords","viewUserActivity","viewUserLoginRecords",
"viewUser","loadConfig","saveConfig","sendTGMessage","viewLoginAttempts","requestsLogs","createSystemUser","syncUsers",
"removeSystemUser","systemUserExists",
"listServers"
]
"""