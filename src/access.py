import requests
import json
import os

class User:
    def __init__(self, email, password, tfa, fingerprint=str(), url=str()):
        self.email = email
        self.password = password
        self.tfa = tfa
        self.fingerprint = fingerprint

    def login(self):
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
