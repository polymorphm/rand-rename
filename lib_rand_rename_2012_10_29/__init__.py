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
import itertools

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
            '--slice-size',
            metavar='SLICE-SIZE',
            type=int,
            help='slice to directories',
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
            nargs='?',
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
    
    prefix = args.prefix if args.prefix is not None else ''
    target = args.target if args.target is not None else args.source
    get_new_path = lambda scheduled_target, name: os.path.join(
            scheduled_target, '{}.{}'.format(name, args.ext))
    assert args.rand_size > 0
    get_rand = lambda: rand(args.rand_size)
    
    assert args.slice_size is None or args.slice_size > 0
    slice_size = args.slice_size
    
    def get_scheduled_iter():
        orig_scheduled_iter = iter(scheduled_list)
        
        if slice_size is None:
            yield orig_scheduled_iter, target
            return
        
        for i in itertools.count():
            scheduled_iter = itertools.islice(orig_scheduled_iter, slice_size)
            scheduled_target = os.path.join(target, str(i))
            
            yield scheduled_iter, scheduled_target
    
    for scheduled_iter, scheduled_target in get_scheduled_iter():
        is_empty = True
        
        for path in scheduled_iter:
            if is_empty:
                is_empty = False
                
                os.makedirs(scheduled_target, exist_ok=True)
                
                print('created dir: {!r}'.format(scheduled_target))
            
            if prefix:
                new_name = '{}-{}-{}'.format(prefix, get_rand(), get_rand())
            else:
                new_name = '{}-{}'.format(get_rand(), get_rand())
            
            new_path = get_new_path(scheduled_target, new_name)
            
            while os.path.exists(new_path):
                new_name = '{}-{}'.format(new_name, get_rand())
                new_path = get_new_path(scheduled_target, new_name)
            
            os.rename(path, new_path)
            
            print('renamed: {!r} => {!r}'.format(path, new_path))
        
        if is_empty:
            break
    
    print('done!')
