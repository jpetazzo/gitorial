#!/usr/bin/env python
import sys
from git import *

repo = Repo(sys.argv[1])
baseurl = sys.argv[2] if sys.argv[2:] else None

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

# If any commit message contains '..' on a single line, use it as a marker
# for file inclusion. Else, include files at the end of each commit.
explicitinclude = any('\n..\n' in commit.message for commit in commits)

output = []
for commit in commits:
    # Prepare the block containing included files.
    filesoutput = ['\n']
    for diff in commit.parents[0].diff(commit):
        filepath = diff.b_blob.path
        if baseurl:
            filesoutput.append('`{0} <{1}/blob/{2}/{3}>`_::\n\n'
                               .format(filepath, baseurl,
                                       commit.hexsha, filepath))
        else:
            filesoutput.append('``{0}``::\n\n'.format(filepath))
        if '\n..\n' in commit.message:
            for line in diff.b_blob.data_stream.read().split('\n'):
                filesoutput.append('  {0}\n'.format(line))
        filesoutput.append('\n')
    filesoutput = ''.join(filesoutput)
    # Now process the commit message itself.
    firstline, nextlines = commit.message.split('\n', 1)
    output.append(firstline)
    output.append('\n')
    output.append(len(firstline)*'-')
    output.append('\n')
    if explicitinclude:
        nextlines = nextlines.replace('\n..\n', filesoutput)
    output.append(nextlines)
    output.append('\n')
    if not explicitinclude or '\n..\n' not in commit.message:
        output.append(filesoutput)
    output.append('\n')

print ''.join(output)
