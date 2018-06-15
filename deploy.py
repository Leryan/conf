#!/usr/bin/env python

import argparse
import os
import shutil


def find_workdir(file_path):
    return os.path.dirname(os.path.abspath(file_path))


class Deployer(object):

    def __init__(self, workdir, deploy_to, simulate, no_deploy_ext):
        self.workdir = os.path.abspath(workdir)
        self.deploy_to = os.path.abspath(deploy_to)
        self.simulate = simulate
        self.no_deploy_ext = no_deploy_ext

        if not os.path.exists(self.deploy_to):
            raise Exception(f'path {deploy_to} does not exists')

    def deploy(self):
        if self.simulate:
            print('SIMULATION')
        else:
            print('DOING TASKS')
        print(f'deploying from: {self.workdir}')
        print(f'deploying to  : {self.deploy_to}')

        self._walk()

    def _truncate(self, path):
        """
        Replace the workdir part with the deploy_to path in path.
        :param str path:
        """
        return path.replace(self.workdir, self.deploy_to)

    def _ensure_dir(self, root, dirname):
        directory = os.path.join(root, dirname)

        if os.path.exists(directory) and not os.path.isdir(directory):
            print(f'unlink not-a-dir {directory}')
            if not self.simulate:
                os.unlink(directory)

        elif os.path.exists(directory):
            print(f'directory {directory} ok')
            return

        print(f'makedirs {directory}')
        if not self.simulate:
            os.makedirs(directory)

    def _ensure_link(self, root, deployroot, filename):
        filepath = os.path.join(root, filename)
        filepath_deploy = os.path.join(deployroot, filename)

        if os.path.isfile(filepath_deploy) or os.path.islink(filepath_deploy):
            print(f'remove old link/file {filepath_deploy}')
            if not self.simulate:
                os.unlink(filepath_deploy)

        print(f'redeploy {filepath_deploy}')
        if not self.simulate:
            os.symlink(filepath, filepath_deploy)

    def _ensure_template(self, root, deployroot, filename):
        filepath_deploy = os.path.join(
            deployroot, filename.replace(self.no_deploy_ext, '')
        )

        if os.path.islink(filepath_deploy):
            print(f'unlink {filepath_deploy} (next action: copy)')
            if not self.simulate:
                os.unlink(filepath_deploy)

        if os.path.isfile(filepath_deploy):
            print(f'{filepath_deploy} already deployed')
            return

        filepath = os.path.join(root, filename)
        print(f'copy {filepath} to {filepath_deploy}')
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
