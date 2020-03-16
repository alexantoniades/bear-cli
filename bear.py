import click
import requests
import os
import json


@click.group(invoke_without_command=False)
@click.pass_context
def bear(context):
    if context.invoked_subcommand is None:
        print('I was invoked without subcommand')
    else:
        print('I am about to invoke %s' % context.invoked_subcommand)


# bear <login>
def accessUser(
    email=str(), 
    password=str(), 
    tfa=int(), 
    fingerprint=str(), 
    url="https://qgg.hud.ac.uk/access/login.php"
) -> requests.Response:
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

class HiddenPassword(object):
    def __init__(self, password=''):
        self.password = password
    def __str__(self):
        return '*' * len(self.password)

@bear.command()
@click.option(
    '--email',
    prompt=True,
    default=lambda: os.environ.get('USER', '')
)
@click.option(
    '--password',
    prompt=True,
    default=lambda: HiddenPassword(os.environ.get('PASSWORD', '')),
    hide_input=True
)
@click.option(
    '--tfa',
    prompt=True,
    default=lambda: os.environ.get('TWOFACTOR', '')
)
@click.option('--confirm', '-y', is_flag=True, default=False)
def login(email, password, tfa, confirm):
    """ 
    Log in as user
    """
    if confirm is not True:
        check = click.prompt('Are you sure you want to login?(y/n)').lower()
        if check in ['y', 'yes']:
            confirm = True
        else:
            confirm = False

    
    if confirm:
        response = json.loads(accessUser(email, password, tfa).text)
        print(response.message)
    else:
        print('exited')


# bear <logout>
@bear.command()
@click.option('--yes', '-y', is_flag=True, default=False)
def logout(yes):
    if yes is not True:
        confirm = click.prompt('Are you sure?(y/n)').lower()
        if confirm in ['y', 'yes']:
            yes = True
        else:
            yes = False

    
    if yes:
        print('logout')
    else:
        print('exited')
    


# bear user
@bear.command()
@click.option('--all', '-a', type=str)
def user(all):
    print('user')


# bear view
@bear.command()
@click.option('--all', '-a', type=str)
def view(all):
    print('view')


# bear <system>
@bear.command()
@click.option('--install', '-i', is_flag=True, default=False)
@click.option('--remove', '-r', is_flag=True, default=False)
def system(install, remove):
    if install:
        print('install')
    elif remove:
        print('remove')
    print('system')


if __name__ == '__main__':
    bear()
