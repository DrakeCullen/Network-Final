#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import re
import sys
import webbrowser

import requests
import requests.exceptions
import kattis
import time

from scipy.fftpack import diff
import configparser

_DEFAULT_CONFIG = '/usr/local/etc/kattisrc'

class ConfigError(Exception):
    pass


def get_url(cfg, option, default):
    return cfg.get('kattis', option)

def get_config():
    """Returns a ConfigParser object for the .kattisrc file(s)
    """
    cfg = configparser.ConfigParser()
    if os.path.exists(_DEFAULT_CONFIG):
        cfg.read(_DEFAULT_CONFIG)

    if not cfg.read([os.path.join(os.path.expanduser("~"), '.kattisrc'),
                     os.path.join(os.path.dirname(sys.argv[0]), '.kattisrc')]):
        raise ConfigError('''\
I failed to read in a config file from your home directory or from the
same directory as this script. To download a .kattisrc file please visit
https://<kattis>/download/kattisrc

The file should look something like this:
[user]
username: yourusername
token: *********

[kattis]
hostname: <kattis>
loginurl: https://<kattis>/login
submissionurl: https://<kattis>/submit
submissionsurl: https://<kattis>/submissions''')
    return cfg

def login(login_url, username, password=None, token=None):
    """Log in to Kattis. Returns a requests.Response with cookies needed to be able to submit
    """
    login_args = {'user': username, 'script': 'true'}
    if password:
        login_args['password'] = password
    if token:
        login_args['token'] = token

    return requests.post(login_url, data=login_args, headers={'User-Agent': 'kattis-cli-submit'})

def login_from_config(cfg):
    """Log in to Kattis using the access information in a kattisrc fil
    Returns a requests.Response with cookies needed to be able to submit
    """
    username = cfg.get('user', 'username')
    password = token = None
    token = cfg.get('user', 'token')
    if password is None and token is None:
        raise ConfigError('''\
Your .kattisrc file appears corrupted. It must provide a token (or a
KATTIS password).

Please download a new .kattisrc file''')

    loginurl = get_url(cfg, 'loginurl', 'login')
    return login(loginurl, username, password, token)


def submit(submit_url, cookies, problem, language, files, mainclass='', tag=''):
    """Make a submission.
    Returns the requests.Result from the submission
    """

    data = {'submit': 'true',
            'submit_ctr': 2,
            'language': language,
            'mainclass': mainclass,
            'problem': problem,
            'tag': tag,
            'script': 'true'}

    sub_files = []
    for f in files:
        with open(f) as sub_file:
            sub_files.append(('sub_file[]',
                              (os.path.basename(f),
                               sub_file.read(),
                               'application/octet-stream')))

    return data, requests.post(submit_url, data=data, files=sub_files, cookies=cookies, headers={'User-Agent': 'kattis-cli-submit'})


def confirm_or_die(problem, language, files, mainclass, tag):
    print('Problem:', problem)
    print('Language:', language)
    print('Files:', ', '.join(files))
    if tag:
        print('Tag:', tag)
    print('Submit (y/N)?')
    if sys.stdin.readline().upper()[:-1] != 'Y':
        print('Cancelling')
        sys.exit(1)


def open_submission(submit_response, cfg, problem_data, cookies,ip):
    submissions_url = get_url(cfg, 'submissionsurl', 'submissions')
    m = re.search(r'Submission ID: (\d+)', submit_response)
    if m:
        submission_id = m.group(1)
        url = '%s/%s' % (submissions_url, submission_id)
        time.sleep(3)
        data={"script":"true"}
        result = requests.get(url,data=data,cookies=cookies)
        if (result.text.find("accepted") == -1):
            print("Rejected")
        else:
            difficulty = requests.get(f"https://open.kattis.com/problems/{problem_data['problem']}").text.split("Difficulty",1)[1][18:21]
            print("Accepted", difficulty)
            print(f"http://{ip}/{difficulty}")
            if ip is not None:
                requests.get(f"http://{ip}/{difficulty}")

def main():
    parser = argparse.ArgumentParser(prog='kattis', description='Submit a solution to Kattis')
    parser.add_argument('-p', '--problem',
                        help=''''Which problem to submit to.''')
    parser.add_argument('-m', '--mainclass',
                        help='''Sets mainclass.''')
    parser.add_argument('-l', '--language',
                        help='''Sets language.''')
    parser.add_argument('-i', '--ip',
                        help='''Sets Candy IP Address.''')
    parser.add_argument('-t', '--tag',
                        help=argparse.SUPPRESS)
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()
    files = args.files
    ip = args.ip
    mainclass = None

    try:
        cfg = get_config()
    except ConfigError as exc:
        print(exc)
        sys.exit(1)

    problem, ext = os.path.splitext(os.path.basename(files[0]))
    language = args.language
    tag = args.tag

    problem = problem.lower()

    if args.problem:
        problem = args.problem

    if args.mainclass is not None:
        mainclass = args.mainclass

    if args.language:
        language = args.language

    if language is None:
        print("No language specified!")
        sys.exit(1)

    files = sorted(list(set(args.files)))

    try:
        login_reply = login_from_config(cfg)
    except ConfigError as exc:
        print(exc)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print('Login connection failed:', err)
        sys.exit(1)

    if not login_reply.status_code == 200:
        print('Login failed.')
        if login_reply.status_code == 403:
            print('Incorrect username or password/token (403)')
        elif login_reply.status_code == 404:
            print('Incorrect login URL (404)')
        else:
            print('Status code:', login_reply.status_code)
        sys.exit(1)

    submit_url = get_url(cfg, 'submissionurl', 'submit')


    confirm_or_die(problem, language, files, mainclass, tag)

    try:
        data, result = submit(submit_url,
                        login_reply.cookies,
                        problem,
                        language,
                        files,
                        mainclass,
                        tag)
    except requests.exceptions.RequestException as err:
        print('Submit connection failed:', err)
        sys.exit(1)

    if result.status_code != 200:
        print('Submission failed.')
        if result.status_code == 403:
            print('Access denied (403)')
        elif result.status_code == 404:
            print('Incorrect submit URL (404)')
        else:
            print('Status code:', result.status_code)
        sys.exit(1)

    plain_result = result.content.decode('utf-8').replace('<br />', '\n')
    print(plain_result)

    try:
        login_reply = login_from_config(cfg)
        open_submission(plain_result, cfg, data,login_reply.cookies,ip)
    except configparser.NoOptionError:
        pass


if __name__ == '__main__':
    main()
