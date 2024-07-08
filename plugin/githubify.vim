" githubify.vim loads and invokes githubify.py.

" Template for utilizing a python function within a vim script is taken from
" https://davidlowryduda.com/writing-a-python-script-to-be-used-in-vim/.

let s:script_dir = fnamemodify(resolve(expand('<sfile>', ':p')), ':h')

function! Githubify(...)
py3 << EOF

import sys
import vim

# Grab arguments passed to the vimscript function.

num_args = int(vim.eval('a:0'))
assert num_args <= 3

if num_args >= 1:
    commit = vim.eval('a:1')
else:
    commit = None

if num_args >= 2:
    use_lineno = int(vim.eval('a:2'))
else:
    use_lineno = True
if use_lineno:
    lineno = vim.current.range.start + 1
else:
    lineno = None

if num_args >= 3:
    base_url = vim.eval('a:3')
else:
    base_url = None

# Load our githubify script.

script_dir = vim.eval('s:script_dir')
sys.path.insert(0, script_dir)

import githubify

# Invoke the script, print the URL, and try to copy to clipboard if we have the
# |pyperclip| module.

url = githubify.githubify(
    abs_filename=vim.current.buffer.name,
    lineno=lineno, commit=commit, base_url=base_url)

print(url)
try:
    import pyperclip
    pyperclip.copy(url)
except ImportError:
    pass
EOF

endfunction

command! -nargs=* Githubify call Githubify(<f-args>)
