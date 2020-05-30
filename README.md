# bear-cli
*A command-line tool for calling the bearicade API (https://github.com/TA3/bearicade).*
## Install
```bash
git clone https://github.com/alexantoniades/bear-cli.git
cd bear-cli
pip3 install -r requirements.txt
alias bear="$(which python3) $(pwd)/bear.py"

bear --help
```
## Usage
### Create profile
```bash
bear add-profile -n <profile name> -k <api key>
```
### Remove profile
```bash
bear remove-profile -n <profile name>
```
### Call API
```bash
bear api -p <profile name> -a <action>
```
