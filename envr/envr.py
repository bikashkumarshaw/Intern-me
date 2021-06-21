import os

##################################################
DEV     = 'dev'

with open(os.path.expanduser('~').replace('/Intern-me', '') + '/.Intern-me/config') as fh:
    ENV_DETAILS = eval(fh.read())

ENV = ENV_DETAILS["ENV"]

# This needs to be better thought out
os.environ['HOME']     = ENV_DETAILS['HOME']

HOME     = os.environ.get('HOME')
DB = ENV_DETAILS['DB']
