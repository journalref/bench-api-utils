from subprocess import check_output, CalledProcessError
from textwrap import dedent


def git_version():
    try:
        revision = check_output(['git', 'rev-parse', 'HEAD'])
    except CalledProcessError:
        revision = 'unknown'

    return revision.strip()[:8]


def git_commit_timestamp():
    try:
        timestamp = check_output(['git', 'show', '-s', '--format=%ct', 'HEAD'])
    except CalledProcessError:
        timestamp = 'unknown'

    return timestamp.strip()


def write_version_module(version, path):
    contents = dedent("""\
    ##################################################
    ###
    ### WARNING
    ###
    ### DO NOT EDIT THIS FILE!!!
    ###
    ### The contents are auto generated by setup.py
    ###
    ##################################################

    version = "%(version)s"
    time_version = "%(time)s"
    git_version = "%(git)s"
    full_version = "{version}-{time_version}-{git_version}".format(**locals())
    """ % dict(
        version = version,
        time = git_commit_timestamp(),
        git = git_version()))

    with open(path, 'w') as fd:
        fd.write(contents)
