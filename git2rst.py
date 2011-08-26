#!/usr/bin/env python
import sys
from git import *

repo = Repo(sys.argv[1])

commits = []
firstcommit = repo.commit('begin')
commit = lastcommit = repo.commit('end')
while commit != firstcommit:
    commits.insert(0, commit)
    if len(commit.parents) > 1:
        raise Exception('Commit {0} has more than one parent!'.format(commit))
    if len(commit.parents) < 1:
        raise Exception('Commit {0} has no parent!'.format(commit))
    commit = commit.parents[0]

output = []
for commit in commits:
    firstline, nextlines = commit.message.split('\n', 1)
    output.append(firstline)
    output.append('\n')
    output.append(len(firstline)*'-')
    output.append('\n')
    output.append(nextlines)
    output.append('\n')
    for diff in commit.parents[0].diff(commit):
        filepath = diff.b_blob.path
        output.append('``{0}``::\n\n'.format(filepath))
        for line in diff.b_blob.data_stream.read().split('\n'):
            output.append('  {0}\n'.format(line))
        output.append('\n')
    output.append('\n')

print ''.join(output)
