#!/usr/bin/env python

import argparse
import os
import shutil

from os.path import isfile, islink, isdir, exists
from os.path import join as pjoin


def find_workdir(file_path):
    return os.path.dirname(os.path.abspath(file_path))


class Deployer(object):

    def __init__(self, workdir, deploy_to, simulate, no_deploy_ext):
        self.workdir = os.path.abspath(workdir)
        self.deploy_to = os.path.abspath(deploy_to)
        self.simulate = simulate
        self.no_deploy_ext = no_deploy_ext

        if not exists(self.deploy_to):
            raise Exception(f'path {deploy_to} does not exists')

    def deploy(self):
        if self.simulate:
            print('SIMULATION')
        else:
            print('DOING TASKS')
        print(f'deploying from: {self.workdir}')
        print(f'deploying to  : {self.deploy_to}')

        self._walk()

    def _log(self, status, msg):
        print(f'{status}: {msg}')

    def _truncate(self, path):
        """
        Replace the workdir part with the deploy_to path in path.
        :param str path:
        """
        return path.replace(self.workdir, self.deploy_to)

    def _ensure_dir(self, root, dirname):
        directory = pjoin(root, dirname)

        if exists(directory) and not isdir(directory):
            self._log('unlink not-a-dir', f'{directory}')
            if not self.simulate:
                os.unlink(directory)

        elif exists(directory):
            self._log('ok', f'directory {directory}')
            return

        self._log('makedirs', f'{directory}')
        if not self.simulate:
            os.makedirs(directory)

    def _ensure_link(self, root, deployroot, filename):
        filepath = pjoin(root, filename)
        filepath_deploy = pjoin(deployroot, filename)

        link_is_file = isfile(filepath_deploy) and not islink(filepath_deploy)
        link_points_ok = islink(filepath_deploy) and os.readlink(filepath_deploy) == filepath

        if link_is_file or not link_points_ok:
            self._log('link', f'{filepath_deploy} -> {filepath}')
            if not self.simulate:
                if exists(filepath_deploy):
                    os.unlink(filepath_deploy)
                os.symlink(filepath, filepath_deploy)
        else:
            self._log('ok', f'{filepath_deploy}')

    def _ensure_template(self, root, deployroot, filename):
        filepath_deploy = pjoin(
            deployroot, filename.replace(self.no_deploy_ext, '')
        )

        if islink(filepath_deploy):
            self._log('unlink', f'{filepath_deploy}')
            if not self.simulate:
                os.unlink(filepath_deploy)

        if isfile(filepath_deploy):
            self._log('template ok', f'{filepath_deploy}')
            return

        filepath = pjoin(root, filename)
        self._log('copy', f'{filepath} -> {filepath_deploy}')
        if not self.simulate:
            shutil.copyfile(filepath, filepath_deploy)

    def _walk(self):
        for rootdir, subdirs, files in os.walk(self.workdir):
            deployroot = self._truncate(rootdir)
            for subdir in subdirs:
                self._ensure_dir(deployroot, subdir)

            for file_ in files:
                if file_.endswith(self.no_deploy_ext):
                    self._ensure_template(rootdir, deployroot, file_)
                else:
                    self._ensure_link(rootdir, deployroot, file_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--deploy-from', default=find_workdir(__file__))
    parser.add_argument('--deploy-to', default=os.environ['HOME'])
    parser.add_argument('--no-deploy-ext', default='.template')
    parser.add_argument('--simulate', action='store_true')

    args = parser.parse_args()

    if args.deploy_to == '':
        parser.error('empty --deploy-to')

    d = Deployer(
        args.deploy_from,
        args.deploy_to,
        args.simulate,
        args.no_deploy_ext
    )
    d.deploy()
