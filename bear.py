import click
import requests
import os
import json
from src.access import User, HiddenPassword


@click.group(invoke_without_command=False)
@click.pass_context
def bear(context):
    if context.invoked_subcommand is None:
        print('I was invoked without subcommand')
    else:
        print('I am about to invoke %s' % context.invoked_subcommand)


# bear <login>
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
        if check in ('y', 'yes'):
            confirm = True
        else:
            confirm = False

    if confirm:
        user = User(email, password, tfa)
        response = user.login()
        print(response.text)
    else:
        print('exited')


# bear <logout>
@bear.command()
@click.option('--yes', '-y', is_flag=True, default=False)
def logout(yes):
    if yes is not True:
        confirm = click.prompt('Are you sure?(y/n)').lower()
        if confirm in ('y', 'yes'):
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
