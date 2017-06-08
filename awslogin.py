#!/usr/bin/env python
"""
A script that can be used to login to AWS via federated login.

This is useful when you have a single account with actual users/passwords and
allow role switching to other accounts.

Your credentials setup should be something like this:

    # ~/.aws/credentials
    [default]
    region = us-east-1
    aws_access_key_id = {yourAccessKeyId}
    aws_secret_access_key = {yourSecretAccessKey}

    [childaccount]
    # X = child account ID
    role_arn = arn:aws:iam::X:role/RoleName
    source_profile = default
    # Y = default account id
    mfa_serial = arn:aws:iam::Y:mfa/UserName
    region = us-east-1
    # optional, but useful to display what the account is
    # I like to use `UserName`.
    role_session_name = UserName
"""

from __future__ import print_function
import argparse
import json
import webbrowser
try:
    from urllib.parse import quote_plus
    from urllib.request import urlopen
except ImportError:
    from urllib import quote_plus, urlopen
import boto3 as aws


def _parse_args(args=None):
    p = argparse.ArgumentParser(description='Log into AWS')
    p.add_argument('profile', help='The AWS profile for which a login should be generated')
    return p.parse_args(args)


def login(session, fetch=urlopen):
    """
    Perform the login dance and return a URL that can be opened in the browser.
    """

    creds = session.get_credentials() # will prompt for MFA
    fed = {
        'sessionId': creds.access_key,
        'sessionKey': creds.secret_key,
        'sessionToken': creds.token,
    }

    url = 'https://signin.aws.amazon.com/federation?Action=getSigninToken&Session={sess}'.format(
        sess=quote_plus(json.dumps(fed))
    )
    resp = fetch(url)
    body = json.loads(resp.read())

    return 'https://signin.aws.amazon.com/federation?Action=login&Issuer=&Destination={dest}&SigninToken={token}'.format(
        dest=quote_plus('https://console.aws.amazon.com/'),
        token=quote_plus(body['SigninToken']),
    )


def main(args=None):
    args = _parse_args(args)
    session = aws.Session(profile_name=args.profile)
    url = login(session)
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    main()
