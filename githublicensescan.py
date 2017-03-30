#!/usr/bin/env python

import re

import requests

re_link = re.compile('^<([^>]*)>; rel="([a-z]*)"$')

def get_next_api_url(headers):
    api_url = ''

    if headers.get('Link', None) is not None:
        links = headers.get('Link').split(', ')
        for link in links:
            m_link = re_link.match(link)

            if m_link is None:
                break

            if m_link.group(2) == 'next':
                api_url = m_link.group(1)
                break

    return api_url

def main():
    github = 'https://api.github.com'
    user = ''
    token = ''

    s = requests.Session()
    s.auth = (user, token)

    api_url = f'{github}/users/{user}/repos?type=owner'
    while api_url != '':
        repos = s.get(api_url)
        api_url = get_next_api_url(repos.headers)

        for repo in repos.json():
            if repo['fork'] == True:
                continue

            repo_name = repo['name']

            content = s.get(f'{github}/repos/{user}/{repo_name}/contents/LICENSE')

            if content.status_code == 404:
                print(f'{repo_name}: missing LICENSE file')

if __name__ == '__main__':
    main()
