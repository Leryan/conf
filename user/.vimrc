" Prerequisites:
"
" system:
"   pacman -S base-devel clang cmake rust the_silver_searcher fzf npm nodejs
"   python-pylint python2-pylint python-jedi python2-jedi flake8
"   python2-flake8 autopep8 python2-autopep8 python-isort python2-isort go
"   python-virtualenv python2-virtualenv
"
"   vim-plug
"
" shell:
"   export FZF_DEFAULT_COMMAND='ag --nocolor -g ""'
"
" :GoInstallBinaries

set nocompatible
set encoding=utf-8
filetype off

call plug#begin('~/.vim/plugged')

Plug 'rust-lang/rust.vim'
Plug 'airblade/vim-gitgutter'
Plug 'tpope/vim-surround'
" press - to get file explorer
Plug 'tpope/vim-vinegar'
" readline shortcuts: saving your life
Plug 'tpope/vim-rsi'
" if -> end and so...
Plug 'tpope/vim-endwise'
" \\w or \\s to quick nav
Plug 'easymotion/vim-easymotion'
" :Grepper, :h grepper
Plug 'mhinz/vim-grepper'
Plug 'tomtom/tcomment_vim'
" install https://github.com/universal-ctags/ctags
" https://andrew.stwrt.ca/posts/vim-ctags
Plug 'majutsushi/tagbar'
Plug 'ap/vim-css-color'
Plug 'w0rp/ale'
Plug 'osyo-manga/vim-over'
Plug 'tpope/vim-fugitive'
Plug 'scrooloose/nerdtree'
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'Valloric/YouCompleteMe', {'dir': '~/.vim/plugged/YouCompleteMe', 'do': './install.py --clang-completer --system-libclang --go-completer --rust-completer --js-completer'}
Plug 'terryma/vim-multiple-cursors'
Plug 'ntpeters/vim-better-whitespace'
Plug 'posva/vim-vue'
Plug 'fisadev/vim-isort'
Plug 'vimjas/vim-python-pep8-indent'
Plug 'fatih/vim-go', {'do': ':GoInstallBinaries'}
Plug 'tpope/vim-sensible'
Plug 'justinmk/vim-sneak'
Plug 'tweekmonster/django-plus.vim'

call plug#end()

let g:sneak#label = 1

let g:acp_enableAtStartup = 1

inoremap <expr><TAB> pumvisible() ? "\<C-n>" : "\<TAB>"

" disable sign column if no error reported
set signcolumn=yes

let g:go_metalinter_autosave = 0
let g:go_metalinter_autosave_enabled = []
let g:go_fmt_command = "goimports"
let g:go_gocode_unimported_packages = 1
let g:go_template_use_pkg = 1
let g:go_highlight_functions = 1
let g:go_highlight_function_calls = 1
let g:go_list_type = "locationlist"
let g:go_fmt_fail_silently = 1

let g:tagbar_autofocus = 1
let g:tagbar_case_insensitive = 1
let g:tagbar_show_linenumbers = 1

let g:racer_experimental_completer = 1

let g:ycm_min_num_of_chars_for_completion = 3
let g:ycm_complete_in_comments = 0
let g:ycm_python_binary_path = 'python'
let g:ycm_autoclose_preview_window_after_insertion = 1
let g:ycm_auto_trigger = 0
let g:ycm_show_diagnostics_ui = 0
let g:ycm_enable_diagnostic_highlighting = 0
let g:ycm_enable_diagnostic_signs = 0

let g:ale_set_loclist = 0
let g:ale_set_quickfix = 0
let g:ale_open_list = 0
let g:ale_keep_list_window_open = 0
let g:ale_completion_enabled = 0
let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 'never'
let g:ale_list_window_size = 5
let g:ale_python_pylint_options = '--load-plugins=pylint_django'

" use Ctrl+j to go through warning and errors
nmap <silent> <C-j> <Plug>(ale_next_wrap)

let g:gitgutter_enabled = 1
let g:gitgutter_signs = 1

let g:fzf_buffers_jump = 1
let g:fzf_command_prefix = 'Fzf'

map <C-n> :NERDTreeToggle<CR>
map <C-p> :FzfFiles<CR>
map <C-b> :FzfBuffers<CR>
map <C-s> :OverCommandLine :%s/<CR>

autocmd FileType go map <F2> :GoRename 
autocmd FileType go map <F3> :GoTestFunc<CR>
autocmd FileType go map <F4> :GoCoverageToggle<CR>

" for ALE but not only, close location list with the associated buffer.
augroup CloseLoclistWindowGroup
	autocmd!
	autocmd QuitPre * if empty(&buftype) | lclose | endif
augroup END

set hidden
set number
set background=dark
set expandtab
set tabstop=4
set shiftwidth=4
set nobackup
set ignorecase
set smarttab
set softtabstop=4
set wildmenu
set wildmode=longest:list
set modeline
set laststatus=2
"set cc=79
set nolist
"set linebreak
set formatoptions+=1
set hlsearch
set ruler
set showcmd
set incsearch
set backspace=indent,eol,start
filetype plugin indent on
syntax on
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
