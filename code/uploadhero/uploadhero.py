#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
# vim: expandtab tabstop=4 shiftwidth=4

import sys
import re
import time
import argparse

from io import BytesIO
import requests

from PIL import Image

class UploadHero:
    def __init__(self, uh_url, user, passwd, debug):
        self.conf = {}
        self.conf['debug'] = debug
        self.conf['user'] = user
        self.conf['passwd'] = passwd
        self.conf['to_read'] = 8192
        self.conf['free_time_wait'] = 60
        self.uh = {}
        self.uh['link'] = {}
        self.uh['link']['url'] = uh_url
        self.uh['link']['base'] = 'http://uploadhero.co/'
        self.uh['link']['dl'] = self.uh['link']['base'] + 'dl/'
        self.uh['link']['dlurl'] = self.uh['link']['dl'] + self.uh['link']['url']
        self.uh['link']['capdl'] = self.uh['link']['base'] + 'captchadl.php?'
        self.uh['link']['connection'] = self.uh['link']['base'] + 'lib/connexion.php'
        self.uh['re'] = {}
        self.uh['re']['capdl'] = re.compile(r'img src="/captchadl\.php\?([0-9a-f]+)"', re.I)
        self.uh['re']['realdl'] = re.compile(r'magicomfg.*href="(http://[^\"]+)"', re.I)
        self.uh['re']['blocked'] = re.compile(r'/lightbox_block_download\.php\?min=([0-9]+)\&sec=([0-9]+)"', re.I)
        self.uh['re']['auth'] = re.compile(r'cookietransitload" style="display:none;">([^<>"]*)<', re.I)

        self.session = requests.Session()

    def _print_log(self, prefix, msg, ret):
        r = '\r' if ret else ''
        e = '\n' if not ret else ''
        sys.stdout.write(r + prefix + msg + e)
        sys.stdout.flush()

    def print_info(self, msg, ret=False):
        self._print_log('[INFO]  ', msg, ret)

    def print_error(self, msg, ret=False):
        self._print_log('[ERROR] ', msg, ret)

    def get_captchadl(self, datas):
        m = self.uh['re']['capdl'].findall(datas)
        try:
            return m[0]
        except IndexError:
            return None

    def get_filelink(self, datas):
        m = self.uh['re']['realdl'].findall(datas)
        try:
            return m[0]
        except IndexError:
            return None

    def display_captcha(self):
        try:
            f_captcha = open('captcha.jpeg', 'bw')
            f_captcha.write(self.captcha_file.getvalue())
            f_captcha.close()
            im = Image.open('captcha.jpeg')
            im.show()
        except:
            self.print_error('''Problem opening captcha.jpeg.
            Do it yourself if you can.''')

    def uh_connect(self):
        post_login = {'pseudo_login': self.conf['user'],
                     'password_login': self.conf['passwd']}
        res = self.session.post(self.uh['link']['connection'], data=post_login)
        m = self.uh['re']['auth'].findall(res.text)
        try:
            self.session.cookies.set('uh',
                m[0].replace("=", "%3D"),
                domain='uploadhero.co',
                expires=None, path='/')
            res = self.session.get(self.uh['link']['base'])
            return res
        except IndexError:
            return None

    def download(self, url, file_name):
        raw_sock = self.session.get(url, stream=True).raw
        f_out = open(file_name, 'bw')
        length = 100
        length_orig = length + 1
        to_read_sub = self.conf['to_read']
        try:
            length = int(raw_sock.getheader('content-length'))
            length_orig = length
        except TypeError:
            to_read_sub = 0
            self.print_error('''No length given, download will
            go on but no percentage will be displayed.''')

        while True:
            data = raw_sock.read(self.conf['to_read'], True)
            if data is b'':
                break
            length -= to_read_sub
            self.print_info('Download completed: ' +
            str(int(100 - length * 100 / length_orig)) +
            '%', True)
            f_out.write(data)
            f_out.flush()
            if length < 1:
                break
        f_out.close()
        print()

    def main(self):
        # Init session and lang cookie
        self.session.cookies.set('lang',
            'en',
            domain='uploadhero.co',
            expires=None, path='/')

        # Get connected to UploadHero
        res = self.uh_connect()
        if res:
            if self.conf['user'] in res.text:
                self.print_info('Authenticated as ' + self.conf['user'] + '.')
        else:
            self.print_error('NOT authenticated.')

        # Connect to the URL we want to DL
        res = self.session.get(self.uh['link']['dl'] + self.uh['link']['url'])

        # Are we blocked ?
        m = self.uh['re']['blocked'].findall(res.text)
        try:
            self.print_error('Blocked for ' +
            m[0][0] + ' minutes and ' +
            m[0][1] + ' seconds.')
            sys.exit(1)
        except IndexError:
            pass

        # Valid captcha
        capdl = self.get_captchadl(res.text)
        if capdl:
            content = self.session.get(self.uh['link']['capdl'] + capdl).content
            self.captcha_file = BytesIO(content)

        # Show captcha and let user enter the code, then send it
            self.display_captcha()
            code = input('[ENTER] Captcha code: ')
            url = self.uh['link']['dlurl'] + '?code=' + code
            res = self.session.get(url)

            if '"dddl"' not in res.text:
                self.print_error('Error in captcha.\n')
                sys.exit(1)
        else:
            self.print_error('Captcha dl link not found.')

        # Get real DL link, valid after 1 minute
        file_link = self.get_filelink(res.text)
        file_name = file_link.split('/')[-1:][0]
        self.print_info('File is: ' + file_name)
        if capdl:
            i = 0
            while i < self.conf['free_time_wait']:
                self.print_info('Download will start in ' +
                str(self.conf['free_time_wait'] - i).zfill(2) +
                ' seconds.', True)
                time.sleep(1)
                i += 1
            print()

        self.download(file_link, file_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', dest='shorturl', required=True)
    parser.add_argument('-U', dest='user')
    parser.add_argument('-P', dest='passwd')
    parser.add_argument('-d', dest='debug', action='store_true')
    args = parser.parse_args()
    uh = UploadHero(args.shorturl, args.user, args.passwd, args.debug)
    uh.main()
