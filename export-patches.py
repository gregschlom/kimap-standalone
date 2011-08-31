#!/usr/bin/env python
import os, shutil

patched_repos = ['kdelibs', 'kdepimlibs']
for repo in patched_repos:
    patch_dir = 'patches/' + repo
    if os.path.isdir(patch_dir):
        shutil.rmtree(patch_dir)
    os.system('cd src/' + repo + ' && git checkout kimap-standalone && git format-patch -N -o ../../patches/' + repo + ' master')
