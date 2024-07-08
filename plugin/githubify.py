import os
import os.path
import subprocess


def _sanitize_origin_url(url):
    if url.endswith('.git'):
        url = url[:url.rindex('.git')]
    # A git url has the form "git@[hostname]:[repo_path]".
    if not (url.startswith('git@') and ':' in url):
        return url
    return 'https://' + url[url.index('@')+1:].replace(':', '/', 1)


def githubify(abs_filename, commit=None, lineno=None, base_url=None):
    cwd = os.path.abspath(os.path.dirname(abs_filename))

    if commit is None:
        commit = 'HEAD'
    commit_sha = subprocess.check_output(['git', 'rev-parse', commit], cwd=cwd).decode('utf-8').strip()

    if base_url is None:
        remote_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], cwd=cwd).decode('utf-8').strip()
        base_url = _sanitize_origin_url(remote_url)

    rel_filename = subprocess.check_output(['git', 'ls-files', '--full-name', abs_filename], cwd=cwd).decode('utf-8').strip()
    lineno_str = '#L{}'.format(lineno) if lineno is not None else ''
    return '{}/blob/{}/{}{}'.format(base_url, commit_sha, rel_filename, lineno_str)
