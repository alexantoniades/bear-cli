import click, os, requests
from tinydb import TinyDB, Query

class ApiDB:
    def __init__(self, path='./profiles/profiles.json'):
        self.path = path
        self.document = TinyDB(path)

    def addAPIKey(self, name, key):
        return(self.document.upsert({'name': name, 'key': key}, Query().name == name))

    def findAPIKey(self, name):
        profile = self.document.search(Query().name == name)
        if len(profile) == 0:
            return('')
        else:
            return(profile[0]['key'])

    def removeAPIKey(self, name):
        return(self.document.remove(Query().name == name))

    @property
    def len(self):
        return(len(self.document))

def callAPI(action, params=dict(), api_key='', url='https://qgg.hud.ac.uk/controller/api.php'):
    """GET requests API: a: action, params: parameters."""
    headers={ 'API_KEY': api_key }
    parameters={ 'a': action, **params }
    return(requests.get(
        url=url,
        headers=headers,
        params=parameters
    ).json())

# Declare database object
db = ApiDB()

@click.group(invoke_without_command=False)
@click.pass_context
def bear(context):
    pass

# bear <add-profile>
@bear.command()
@click.option(
    '--name', '-n',
    prompt=True
)
@click.option(
    '--key', '-k',
    prompt=True
)
def add_profile(name, key):
    """Adds profile from name and key"""
    db.addAPIKey(name, key)
    click.echo(f"'{name}' profile added")


# bear <remove-profile>
@bear.command()
@click.option(
    '--name', '-n',
    prompt=True
)
@click.option('--confirm', '-y', is_flag=True, default=False)
def remove_profile(name, confirm):
    """Removes profile by name"""
    if confirm:
        db.removeAPIKey(name)
        click.echo(f"'{name}' profile removed")
    else:
        click.echo(f"'{name}' profile not removed")

# bear <api>
@bear.command()
@click.option(
    '--profile', '-p',
    prompt=True
)
@click.option(
    '--action', '-a',
    prompt=True
)
@click.option(
    '--user', '-u',
    type=None
)
def api(profile, action, user):
    """GET request <action> to api adding key stored in profiles"""
    key = db.findAPIKey(profile)
    if key == '':
        click.echo('Profile does not exists')
    else:
        if user is not None:
            user = {}
        else:
            user = { 'u': user }
        click.echo(str(callAPI(action, user, api_key=key)))

if __name__ == '__main__':
    bear()
