import os
import os.path
import subprocess

def githubify(abs_filename, lineno=None, commit=None, base_url=None, base_dir=None):
    if commit is None:
        commit = 'HEAD'
    commit_sha = subprocess.check_output('git rev-parse {0}'.format(commit).split()).decode('utf-8').strip()
    if base_url is None:
        base_url = os.environ['GITHUBIFY_BASE_URL']
    if base_dir is None:
        base_dir = os.getcwd()
    rel_filename = os.path.relpath(abs_filename, base_dir)
    lineno_str = '#L{}'.format(lineno) if lineno is not None else ''
    return '{}/blob/{}/{}{}'.format(base_url, commit_sha, rel_filename, lineno_str)
