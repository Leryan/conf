#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Florent Peterschmitt <florent@peterschmitt.fr>

import json
import sys
import subprocess
import shlex
import os
import requests
import argparse

class CmdException(Exception):
    pass

class APIError(Exception):
    pass

def exec_cmd(cmd, ignore_error=False):
    cmds = shlex.split(str(cmd))
    proc = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.stderr.write(str(proc.stderr, encoding='utf-8'))
        sys.stdout.write(str(proc.stdout, encoding='utf-8'))
        sys.stdout.flush()
        sys.stderr.flush()
        if ignore_error == False:
            raise CmdException(cmd)

    return proc

parser = argparse.ArgumentParser()
parser.add_argument('-c', dest='conffile', default='mirror.json')
args = parser.parse_args()

s = requests.Session()
with open(args.conffile, 'r') as fh_conffile:
    conf = json.load(fh_conffile)

os.chdir(conf['workdir'])

print('=> listing projects')
for gitlab in conf['gitlab'].keys():
    url = conf['gitlab'][gitlab]['url']
    tok = conf['gitlab'][gitlab]['token']
    r = s.get(f"{url}/projects?per_page=100000&private_token={tok}")

    if not r.ok:
        raise APIError(r.content)

    conf['gitlab'][gitlab]['projects'] = r.json()

def project_exists(projects, project_name, namespace, namespace_kind):
    namespace_id = None
    project_id = None

    for project in projects:
        pns = project['namespace']['name']
        pnsk = project['namespace']['kind']
        if pns == namespace and pnsk == namespace_kind:
            namespace_id = project['namespace']['id']
            project_id = project['id']

            if project['name'] == project_name:
                return True, namespace_id, project_id

    return False, namespace_id, None

for project in conf['gitlab'][conf['source']]['projects']:
    project_name = project['name']
    project_ns = project['namespace']['name']
    project_nsk = project['namespace']['kind']

    if project_ns != conf['namespace'] or project_nsk != conf['namespace_kind']:
        continue

    print(f'=> working on {project_name}')

    for gitlab in conf['gitlab'].keys():
        if gitlab == conf['source']:
            continue

        pe = project_exists(conf['gitlab'][gitlab]['projects'], project_name, project_ns, project_nsk)
        url = conf['gitlab'][gitlab]['url']
        token = conf['gitlab'][gitlab]['token']
        import_url = None
        if conf['gitlab'][gitlab].get('mirror_base', False) != False:
            import_url = '{}/{}/{}.git'.format(
                conf['gitlab'][gitlab]['mirror_base'],
                project_ns,
                project_name
            )

        if pe[0] == False:
            print(f'==> create project on {gitlab}')
            data = {
                'name': project_name,
                'namespace_id': pe[1],
                'description': project['description']
            }
            if import_url is not None:
                data['import_url'] = import_url
            r = s.post(f'{url}/projects?private_token={token}', data=data)

        elif import_url is not None:
            print('==> configure import_url')
            data = {
                'name': project_name,
                'import_url': import_url
            }
            r = s.put(f"{url}/projects/{pe[2]}?private_token={token}", data=data)

        if not r.ok:
            raise APIError(r.content)

    if not os.path.isdir(f'{project_name}.git') and conf['push_pull'] == True:
        print('==> cloning project')
        project_url = '{}/{}/{}.git'.format(conf['gitlab'][conf['source']]['clone'], project_ns, project_name)
        cmd = f'git clone --mirror {project_url}'
        exec_cmd(cmd)

    if os.path.isdir(f'{project_name}.git') and conf['push_pull'] == True:
        os.chdir(f'{project_name}.git')

        print('==> fix remotes')
        for gitlab in conf['gitlab'].keys():
            remote = gitlab

            if gitlab == conf['source']:
                remote = 'origin'

            cmd = f'git --bare remote remove {remote}'
            exec_cmd(cmd, True)

            cmd = 'git --bare remote add {} "{}/{}/{}.git"'.format(
                remote,
                conf['gitlab'][gitlab]['clone'],
                project_ns,
                project_name
            )
            exec_cmd(cmd)

        cmd = 'git --bare config remote.origin.fetch \'refs/*:refs/*\''
        exec_cmd(cmd)
        
        cmd = 'git --bare config remote.origin.mirror true'
        exec_cmd(cmd)

        print('==> fetch latest commits from master')
        cmd = f'git --bare fetch -p origin'
        exec_cmd(cmd)

        for gitlab in conf['gitlab'].keys():
            if gitlab == conf['source']:
                continue

            print(f'==> pushing {project_name} to remote {gitlab}')
            cmd = f'git --bare push --mirror {gitlab}'
            exec_cmd(cmd)

        os.chdir('..')
