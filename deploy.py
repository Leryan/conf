#!/usr/bin/env python

import argparse
import os
import shutil

from os.path import isfile, islink, isdir
from os.path import lexists as exists
from os.path import join as pjoin


def find_workdir(file_path):
    return os.path.dirname(os.path.abspath(file_path))


class States:

    LINK = 'link'
    UNLINK = 'unlink'
    OK = 'ok'
    TOK = 'template ok'
    COPY = 'copy'
    MAKEDIRS = 'makedirs'
    SKIP = 'SKIP'
    WARNING = 'WARNING'


class Deployer(object):

    def __init__(self, deploy_from, deploy_to, simulate, template_ext, force_rmtree):
        """
        :param str deploy_from: where to work from
        :param str deploy_to: consider this path as the root where to deploy files
        :param bool simulate: do not do any action
        :param str template_ext: template extention to be removed when copying
        :param bool force_rmtree: do not ask for directory deletion before link/copy
        """
        self.deploy_from = os.path.abspath(deploy_from)
        self.deploy_to = os.path.abspath(deploy_to)
        self.simulate = simulate
        self.template_ext = template_ext
        self.force_rmtree = force_rmtree

        if not os.path.exists(self.deploy_from):
            raise Exception(f'path {deploy_from} does not exists or is a broken symlink')

        if not os.path.exists(self.deploy_to):
            raise Exception(f'path {deploy_to} does not exists or is a broken symlink')

    def deploy(self):
        if self.simulate:
            print('SIMULATION')
        print(f'deploying from: {self.deploy_from}')
        print(f'deploying to  : {self.deploy_to}')

        self._walk()

    def _log(self, status, msg):
        print(f'{status}: {msg}')

    def _ask_rmtree(self, path):
        """
        :param str path: path to remove recursively
        :rtype bool:
        :returns: True if path was removed, False otherwise
        """
        if not self.force_rmtree:
            answer = input(f'removing {path} directory and any files, confirm? (Y/N): ')
            if answer != 'Y':
                self._log(States.SKIP, f'{path}')
                return False
        else:
            self._log(States.WARNING, f'directory {path} removed without confirmation')

        if not self.simulate:
            shutil.rmtree(path)
            return True

        return False

    def _truncate(self, path):
        """
        Replace the deploy_from part with the deploy_to path in path.
        :param str path:
        """
        return path.replace(self.deploy_from, self.deploy_to)

    def _ensure_dir(self, root, dirname):
        directory = pjoin(root, dirname)

        if exists(directory) and not isdir(directory):
            self._log(States.UNLINK, f'{directory}')
            if not self.simulate:
                os.unlink(directory)

        elif exists(directory):
            self._log(States.OK, f'directory {directory}')
            return

        self._log(States.MAKEDIRS, f'{directory}')
        if not self.simulate:
            os.makedirs(directory)

    def _ensure_link(self, src, dst):
        """
        :param str src: file to point to
        :param str dst: symlink destination
        """
        link_points_ok = islink(dst) and os.readlink(dst) == src
        link_exists = exists(dst)

        if link_points_ok:
            self._log(States.OK, f'{dst}')
            return

        self._log(States.LINK, f'{dst} -> {src}')
        if not self.simulate:
            if link_exists and isdir(dst):
                if not self._ask_rmtree(dst):
                    return

            elif link_exists:
                os.unlink(dst)

            os.symlink(src, dst)

    def _ensure_template(self, src, dst):
        """
        :param str src: file to copy
        :param str dst: where to copy
        """
        dst = dst.replace(self.template_ext, '')

        if islink(dst):
            self._log(States.UNLINK, f'{dst}')
            if not self.simulate:
                os.unlink(dst)

        elif isdir(dst):
            self._log(States.UNLINK, f'{dst}')
            if not self._ask_rmtree(dst):
                return

        elif isfile(dst):
            self._log(States.TOK, f'{dst}')
            return

        self._log(States.COPY, f'{src} -> {dst}')
        if not self.simulate:
            shutil.copyfile(src, dst)

    def _walk(self):
        for rootdir, subdirs, files in os.walk(self.deploy_from):
            deployroot = self._truncate(rootdir)
            for subdir in subdirs:
                self._ensure_dir(deployroot, subdir)

            for file_ in files:
                src = pjoin(rootdir, file_)
                dst = pjoin(deployroot, file_)

                if file_.endswith(self.template_ext):
                    self._ensure_template(src, dst)
                else:
                    self._ensure_link(src, dst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--deploy-from', default=find_workdir(__file__))
    parser.add_argument('--deploy-to', default=os.environ['HOME'])
    parser.add_argument('--template-ext', default='.template')
    parser.add_argument('--simulate', action='store_true')
    parser.add_argument('--force-rmtree', action='store_true', help='if a directory must be replaced by a file or symlink, do not ask for deletion')

    args = parser.parse_args()

    if args.deploy_to == '':
        parser.error('empty --deploy-to')

    d = Deployer(
        args.deploy_from,
        args.deploy_to,
        args.simulate,
        args.template_ext,
        args.force_rmtree,
    )
    d.deploy()
