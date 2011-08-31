Turning git history into a step-by-step tutorial
================================================

This is a meta-tutorial. No, don't run, come back! It is just
*a tutorial explaining how to make tutorials*.

The main idea is to use git commits as the base material for your tutorial.
You start with some existing repository (or from a blank one), and you
start modifying files. You commit your changes with git, and in the commit
message, you include a good amount of text, explaining everything you did
in great lengths. Each significant step of your tutorial corresponds to
a git commit.

Once you're done, you can:

* review everything you did using a special ``git log`` command, which
  will display all the steps of your tutorial in chronological order,
  showing your explanations (=commit messages) along with the changed
  files;
* push to GitHub, and see the same thing using the GitHib "change view":
  this will show all the steps (=commits) of your tutorial in kind of
  table of contents, each commit being clickable and taking the viewer
  to a detailed view;
* generate a RST file with the supplied script, and include this RST
  file in a Wiki or other documentation; for instance, if you use Sphinx
  for your global documentation, you can include the RST (maybe with
  minor documentation) and Sphinx can then transform it into HTML, PDF, etc.

A few examples:

* http://github.com/jpetazzo/thin


Place the begin tag
-------------------

First, we need to place our ``begin`` tag. It's important to remember that
when you give a range to git, the diff of the first commit in the range
won't be included in the output. Therefore, we need to place our ``begin``
tag right before the first step of our tutorial. If we start from an existing
repository, we just have to tag the HEAD of the repository, and all further
commits will make it into our tutorial. If we start from an empty repository,
we need to create a dummy first commit (that cannot be included into our
tutorial) and tag it, just for that purpose.

So, when starting from an existing repository::

  # Clone it or whatever.
  git clone .../something
  cd something
  # Tag the starting point of the tutorial.
  git tag begin

And when starting from scratch::

  # Create a new repository.
  git init helloworld
  cd helloworld
  # Create a dummy empty commit.
  git commit --allow-empty --allow-empy-message -m ''
  # Tag it.
  git tag begin


Write your tutorial
-------------------

Then, start writing the meat of our tutorial. The main point is to use one
commit for each step. If one step involves creating or modifying multiple
files, you can of course group those modifications in one single commit.
Conversely, if multiple sections in a single file deserve distinct parts
in the tutorial, you can do a first round of modification, commit, then
do more changes, and commit again.

Each commit message should start with a title line (try to keep it as short
as possible, around maybe 40 characters, or it will be truncated when
displayed in GitHib change view. Also, if you use the RST output to generate
HTML, the titles will probably look weird if they are too long and span
multiple lines.

If you plan to use the RST output, your commits should be in RST. You don't
have to include underline symbols after the first title line: the RST
generator will take care of that for you.

If you think you got wrong one of your commits or commit messages, don't
worry and have a look at the next paragraph.


Modifications
-------------

If you want to modify your tutorial, you will be using git's history editing
feaetures to change existing commits and commit messages. While some people
use history editing commands all the time, some of you might not be familiar
with that; so here is a really quick and dirty tutorial!

Start by running ``git rebase -i begin``: git will start your editor
and display your commits. You can change their order; but be warned:
while it's easy and straightforward to switch two independent commits
(e.g. commits adding or modifying different sets of files), other
modifications might involve conflict resolution (not covered here).

As shown in the editor, you can prefix each commit with e.g. ``reword``
or ``edit``. ``reword`` will automatically start an editor allowing
to change this commit's message. ``edit`` will allow you to change
the commit. It can also be used to insert new commits, or split the
commit.

To add something to a commit, flag it with ``edit``. Save and exit.
Git will take you to this commit. You can modify files, stage them with
``git add``, and finally run ``git commit --amend``. This will "blend" your
changes with the existing commit.

To change a commit, flag it with ``edit``. Save and exit.
Git will take you to this commit. Then use ``git reset HEAD``: this
will "undo" the commit. You can now do other modifications, and end
with ``git commit``.

To split a commit, follow the same procedure as previously, but
commit multiple times.

Once you're done with editing, run ``git rebase --continue``, and
git will take you back to the tip of the repository.

To see what your tutorial looks like, you can run the following command::

  git log --patch --reverse begin..HEAD


Place the end tag
-----------------

When you are done with the last step of your tutorial, you should add
the ``end`` tag. It will be used by miscellaneous tools to know that
there is nothing useful (for the tutorial) after this tag.

Just run ``git tag end``. That's all!

.. warning::

   If you do some modifications, the hashes of the commits will change
   and the ``end`` tag won't point anymore to the right commit: it
   will point to the commit in the old history.

   To recreate the tag at the right place, you have to delete the old
   tag with ``git tag -d end``, and then run ``git tag end abcd...``,
   where ``abcd...`` is the new hash of the last commit of your tutorial.


Add README and other files
--------------------------

If you plan to push to GitHib, it might be nice to add a README in one
of the supported formats. You might also want to add extra files that
you don't want to include in the tutorial, but that could be useful
(or even necessary) in the repository.

We could have added everything *before* the ``begin`` tag, and not use
a ``end`` tag. However, defining the ``end`` tag and adding those extra
files after it allow to modify them afterward, without rewriting the
whole git history.

On the other hand, if you think that you will most likely not change
those files, but that you will probably update the tutorial itself,
it is certainly better to include the extra files before the ``begin``
tag. That way, a tutorial modification won't rewrite history for the
extra files.

If you include a README file, we suggest that you remind the reader
that the repository itself is a tutorial, and mention the convenient
``git log --patch --reverse begin..end`` command. If you plan to push
to GitHub, you can also mention the nice "change view" URL
(http://github.com/<username>/<reponame>/changes/begin..end).
Last thing: if you plan to use the RST generator, and transform the
output to HTML, you can host the HTML and include a link to the HTML
version. The HTML version will probably be less confusing for people
not used to GitHub.


Push to GitHub
--------------

Push your repository as you would push any other repository.

Don't forget to also push your tags (``git push --tags``).

Dependencies
------------

Before you can run the git2rst.py script you'll need to install the
GitPython module, you can do that by:

``pip install GitPython``


Generate RST output
-------------------

The enclosed git2rst.py script will transform the sequence of commits
of your tutorial into a RST file, as explained above. Each commit
will be one section, and the changed files will be shown at the end
of each section.

The usage of the script is something like this (using our example):

``python git2rst.py helloworld``

It is recommended to add a title and introductory text to the generated
RST output. If you plan to regenerate the RST content frequently,
you might want to put the title and introduction in a separate file,
and include the generated RST content from this separate file.

The RST output can be converted to HTML using e.g. Sphinx.


Updates
-------

If you want to change anything in your tutorial, just do modifications
to the repository as explained above. However, there are a few important
things that you should keep in mind:

* when pushing your repository, you will have to ``git push --force``
  (and push the tags with ``git push --tags --force`` as well), since
  we're basically rewriting history;
* if you're just modifying the README, don't amend the commit, but create
  a new one; because GitHub might not detect that there is a new HEAD
  and still show the old README (and using begin..end tags will usually
  keep the README commits our of your tutorial anyway).


TODO
----

* generate output in other formats (trivial to implement if you need them)
* implement nicer formatting for the files shown at the end of each commit
  (get some inspiration from the way files are shown in e.g. Gist)
* use gitorial for this tutorial


History
-------

I initially wrote this because I wanted people to be able to clone the
code of my tutorials, but I also wanted to generate a "user-friendly"
document. And I did not want the code and the documentation to get out
of sync.

After writing this, I had to come up with a name; and thought that
"gitorial" would be satisfactory. I then found out that there were already
other "gitorial" projects out there. Since the motivations seem to be the
same, I hope nobody will mind if I use the same name!

