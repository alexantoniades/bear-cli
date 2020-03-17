import requests, pyotp

login = None
activity = None
api_key = 'NzI=.67be3ff3bb7ca9105e05eb60aee39a46'
with requests.Session() as s:
    login = s.post(
        url='https://qgg.hud.ac.uk/access/login.php',
        # headers={
        #     'User-Agent': 'Mozilla/5.0'
        # },
        data={
            'email': 'u1674219@unimail.hud.ac.uk',
            'password': 'Fuckordie123',
            'tfaCode': pyotp.TOTP('43AOECFQXRPF6TKQZIITC2WOSUBUXDVD').now(),
            'fp': ''
        }
    )
    activity = s.get(
        'https://qgg.hud.ac.uk/controller/api.php',
        headers={
            'API_KEY': api_key
        },
        params={
            'a': 'listActivity'
        }
    )