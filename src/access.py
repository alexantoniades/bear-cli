import requests
import json
import os
import pyotp
import bcrypt

"""
API actions = [
"blockedAttempts",
"userBehaviour","listActivity","listUsers","listDistinctIPs","deleteUser","toggleUserActive","listGroups","createGroup","deleteGroup",
"sessionsCount","onlineUsersCount","failsCount","AICount","sessionsGeo","viewUserBrowserRecords","viewUserActivity","viewUserLoginRecords",
"viewUser","loadConfig","saveConfig","sendTGMessage","jsonNeuralNetwork","viewLoginAttempts","requestsLogs","createSystemUser","syncUsers",
"removeSystemUser","systemUserExists",
"listServers"
]
"""

class User:
    def __init__(self, email, password, tfa, fingerprint=str(), url=str(), base_url=str()):
        self.email = email
        self.__password = password
        self.tfa = tfa
        self.__fingerprint = fingerprint
        self.base_url = base_url

    def login(self, email, password, tfa, fingerprint, url):
        """
        Provides access to the url
        """
        headers = { 'User-Agent': 'Mozilla/5.0' }
        session = requests.Session()
        response = session.post(url, headers=headers, data={
            'email': email,
            'password': password,
            'tfaCode': tfa,
            'fp': fingerprint
        })
        return(response)

    def logout(self):
        return()

    @property
    def fingerprint(self):
        return(self.__fingerprint)

    @property
    def password(self):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.__password.encode('utf8'), salt)
        return(hashed)

    def getIP(self):
        pass

    
user = User(
    'email@email.com', 
    'password', 
    '12465', 
    fingerprint="nfsonfisgbesr16541g65e14g61s"
)