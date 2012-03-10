" Use Vim settings, rather then Vi settings (much better!).

set nocompatible

" Turn on the verboseness to see everything vim is doing.
"set verbose=9

" allow backspacing over everything in insert mode
set backspace=indent,eol,start


" I like 4 spaces for indenting
set shiftwidth=4

" I like 4 stops
set tabstop=4

" Spaces instead of tabs

set expandtab

" Always  set auto indenting on
set autoindent

" Use Vim settings, rather then Vi settings (much better!).
set nocompatible

" line numbers on
set number

":nnoremap <Leader>s :%s/\<<C-r><C-w>\>/

:nmap <F2> :w\|!python %<cr>
:imap <F2> <Esc>:w\|!python %<cr>
