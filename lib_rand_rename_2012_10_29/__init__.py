# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2012 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import argparse
import os, os.path
import random

def rand(size):
    r = str(random.randrange(10 ** size))
    
    while len(r) < size:
        r = '0{}'.format(r)
    
    return r

def main():
    parser = argparse.ArgumentParser(
        description='utility for renaming files to random name')
    
    parser.add_argument(
            '--prefix',
            metavar='NEW-PREFIX',
            help='create new prefix',
            )
    
    parser.add_argument(
            '--rand-size',
            metavar='CUSTOM-RANDOM-SIZE',
            type=int,
            default=5,
            help='use custom random size. default is 5',
            )
    
    parser.add_argument(
            'ext',
            metavar='EXTENSION',
            help='extension of files',
            )
    
    parser.add_argument(
            'source',
            metavar='SOURCE-PATH',
            help='source directory path',
            )
    
    parser.add_argument(
            'target',
            metavar='TARGET-PATH',
            help='target directory path',
            )
    
    args = parser.parse_args()
    
    scheduled_list = []
    
    for dirpath, dirnames, filenames in os.walk(args.source):
        for filename in filenames:
            if not filename.endswith('.{}'.format(args.ext)):
                continue
            
            path = os.path.join(dirpath, filename)
            scheduled_list.append(path)
            
            print('scheduled: {!r}'.format(path))
    
    os.makedirs(args.target, exist_ok=True)
    
    prefix = args.prefix if args.prefix is not None else ''
    get_new_path = lambda name: os.path.join(
            args.target, '{}.{}'.format(name, args.ext))
    assert args.rand_size > 0
    get_rand = lambda: rand(args.rand_size)
    
    for path in scheduled_list:
        if prefix:
            new_name = '{}-{}-{}'.format(prefix, get_rand(), get_rand())
        else:
            new_name = '{}-{}'.format(get_rand(), get_rand())
        
        while os.path.exists(get_new_path(new_name)):
            new_name = '{}-{}'.format(new_name, get_rand())
        
        os.rename(path, get_new_path(new_name))
        
        print('renamed: {!r} => {!r}'.format(path, get_new_path(new_name)))
