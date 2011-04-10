#!/usr/bin/env python
import os,sys

print 'WARNING: This command will destroy the branch kimap-standalone in src/kdelibs and src/kdepimlib and re-create them from the patches in the patches directory.'
print ''
print 'Every commit in those branches not exported as a patch or cherry-picked somewhere else will be lost'
print ''
answer = raw_input('Do you want to continue? [y/n]')

if answer.lower().startswith('y'):
    patched_repos = ['kdelibs', 'kdepimlibs']
    for repo in patched_repos:
        os.system('cd src/' + repo + ' && git checkout master && git branch -D kimap-standalone')
        os.system('cd src/' + repo + ' && git checkout -b kimap-standalone && git am ../../patches/' + repo + '/*')
else:
    print 'Operation canceled'