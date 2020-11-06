#!/bin/python

# -*- coding: utf-8 -*-

# (c) 2020, cytopia <parhamzardoshti@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
module: FindFile
author: Parham Zardoshti (@scietechso)
short_description: to find all files that we have specified with file formats in src directory (recursively) and put them in given destination directory

description:
    - FindFile module can Find Files with given formats like .exe, txt, mp4, etc and backup them into given directory.
    - More examples at U(https://github.com/lintechso/AnsibleModule)
version_added: "2.9.11"
'''
EXAMPLES = '''
# Find Files with given formats and copy them to given destination
- hosts: localhost
  tasks:
    - name: Find *.txt and *.yml in /opt/test for Backups
      FindFile: src=/opt/test/ dest=/tmp/ formats={{ item }}
      with_items:
        - ".txt"
        - ".yml"
      register: result
    - debug: var=result'''
# FindFile dependencies
from ansible.module_utils.basic import *
from progress.spinner import Spinner
from progress.bar import Bar
import os, sys, shutil

def FindFiles(path,extensions):
    load_state = 0
    path = "%s" % path
    spinner = Spinner('Finding Files ')
    while load_state != 'FINISHED':
        f = open("./logs/log.txt", "a")
        cnt = 0
        for root, dirs, files in os.walk(path):   
            for file in files:
                if file.endswith(extensions):
                        TARGET = os.path.join(root, file)
                        cnt += 1
                        f.write(TARGET+'\n')
                        spinner.next()
        f.close()
        load_state = 'FINISHED'
        chnge = "Found {} files".format(cnt)
        f = open("./logs/cnt.txt", "w")
        f.write(str(cnt))
        f.close()
        return chnge

def StartFunc(src, dest, formats):
    res = dict()
    chng = FindFiles(src,formats)
    f = open("./logs/cnt.txt", "r")
    cnt = f.read()
    f.close()
    with Bar('Copying', max=int(cnt)) as bar:
        filepath = './logs/log.txt'
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                filename = line.strip()
                try:
                    shutil.copy2(filename, dest) 
                    res = dict(
                            changed=True,
                            original_message='Changed',
                            message=chng
                    )
                    #shutil.copy2('/src/file.ext', '/dst/dir') # target filename is /dst/dir/file.ext
                except Exception:
                    res = dict(
                            changed=False,
                            original_message='Error has occured',
                            message=chng
                    )
                line = fp.readline()
                bar.next()
    return res
    fp.close()
# main body
def main():
    fields = { 
        "src": { "requierd": True, "type": "str" },
        "dest": { "requierd": True, "type": "str" },
        "formats": { "requierd": True, "type": "str" }
    }   
    module = AnsibleModule(argument_spec=fields)
    src = os.path.expanduser(module.params['src'])
    dest = os.path.expanduser(module.params['dest'])
    formats = os.path.expanduser(module.params['formats'])
    result = StartFunc(src,dest,formats)
    #remove cnt
    os.system("rm -rf ./logs/")
    #show result
    module.exit_json(**result)
    

if __name__ == '__main__':
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
        os.mknod("./logs/log.txt")
    main()
    
    
