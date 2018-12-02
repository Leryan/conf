PROMPT_COMMAND=__prompt_command

_SYSTEMD_VERSION=""

if [ -f ~/.bash_params ]; then
    source ~/.bash_params
fi

_INTERACTIVE=0
case "$-" in
    *i*)_INTERACTIVE=1;;
    *);;
esac

if [ -z ${XDG_RUNTIME_DIR} ]; then
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
fi

# bash behavior
export HISTCONTROL=ignoreboth:erasedups
shopt -s checkwinsize
shopt -s histappend

# exports
export FZF_DEFAULT_COMMAND='ag --nocolor -U -g ""'
export AURDEST="${HOME}/doc/pacaur"
export XMODIFIERS=emacs
export EDITOR=vim
export PAGER=less
if [ -z "$GOPATH" ]; then
    export GOPATH="$HOME/doc/go"
    export PATH="$PATH:$GOPATH/bin"
fi
export PATH="$PATH:$HOME/.cargo/bin:~/.local/bin"
export PERL5LIB="$HOME/doc/perl5"

# functions
if [ "${_INTERACTIVE}" = "1" ]; then

txtblk="\[\033[0;30m\]" # Black - Regular
txtred="\[\033[0;31m\]" # Red
txtgrn="\[\033[0;32m\]" # Green
txtylw="\[\033[0;33m\]" # Yellow
txtblu="\[\033[0;34m\]" # Blue
txtpur="\[\033[0;35m\]" # Purple
txtcyn="\[\033[0;36m\]" # Cyan
txtwht="\[\033[0;37m\]" # White
bldblk="\[\033[1;30m\]" # Black - Bold
bldred="\[\033[1;31m\]" # Red
bldgrn="\[\033[1;32m\]" # Green
bldylw="\[\033[1;33m\]" # Yellow
bldblu="\[\033[1;34m\]" # Blue
bldpur="\[\033[1;35m\]" # Purple
bldcyn="\[\033[1;36m\]" # Cyan
bldwht="\[\033[1;37m\]" # White
unkblk="\[\033[4;30m\]" # Black - Underline
undred="\[\033[4;31m\]" # Red
undgrn="\[\033[4;32m\]" # Green
undylw="\[\033[4;33m\]" # Yellow
undblu="\[\033[4;34m\]" # Blue
undpur="\[\033[4;35m\]" # Purple
undcyn="\[\033[4;36m\]" # Cyan
undwht="\[\033[4;37m\]" # White
bakblk="\[\033[40m\]"   # Black - Background
bakred="\[\033[41m\]"   # Red
bakgrn="\[\033[42m\]"   # Green
bakylw="\[\033[43m\]"   # Yellow
bakblu="\[\033[44m\]"   # Blue
bakpur="\[\033[45m\]"   # Purple
bakcyn="\[\033[46m\]"   # Cyan
bakwht="\[\033[47m\]"   # White
txtrst="\[\033[0m\]"    # Text Reset

function __cache_systemd_version() {
    if [ ! "${_SYSTEMD_VERSION}" = "" ]; then
        return
    fi

    if [ -f /usr/bin/systemctl ]; then
        _SYSTEMD_VERSION=$(systemctl --version|head -n 1|cut -f2 -d' ')
    else
        _SYSTEMD_VERSION=0
    fi
}

function __git_ps1() {
    git branch > /dev/null 2>&1
    if [ "$?" = "0" ]; then
        local branch=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
        echo "${branch} "
    fi
}

function __tmux() {
    if [ ! -z "${TMUX}" ]||[ "${TERM}" = "screen" ]; then
        return
    fi
    return
    tmux list-sessions > /dev/null 2>&1
    if [ ! "$?" = "0" ]&&[ -z "${TMUX}" ]; then
        __cache_systemd_version
        if ((${_SYSTEMD_VERSION} >= 232)); then
            systemd-run --user --scope tmux
        else
            tmux
        fi
    elif [ -z "${TMUX}" ]; then
        tsessions=$(tmux list-sessions|wc -l)
        if [ "${tsessions}" = 1 ]; then
            tmux a
        else
            tmux list-sessions
        fi
    fi
}

function __tmux_ps1() {
    local tscolor=""
    local symbol="\xe2\x8c\x97"

    return

    tmux list-sessions > /dev/null 2>&1

    if [ "$?" = "0" ]; then
        local tc=$(tmux list-sessions | wc -l)
        if ((${tc} > 10)); then
            tscolor=${txtred}
        elif ((${tc} > 1)); then
            tscolor=${txtgrn}
        else
            tscolor=${txtwht}
        fi
        if [ "${_BP_TERM_UTF8}" = "0" ]; then
            symbol="#"
        fi
        echo -n "${tscolor}${symbol} "
    else
        echo -n ""
    fi
}

function __netns_ps1() {
    local cur_netns=$(ip netns | grep -v id)
    if [ ! "${cur_netns}" = "" ]; then
        echo -n "${cur_netns} "
    fi
}

function dbash() {
    docker run -ti --entrypoint /bin/bash $@
}

function fuck() {
    local last_cmd=$(history -p !!)
    echo -n "run command '${last_cmd}' with sudo? [Y/n]: "
    read -s -n 1 confirm
    echo ""
    if [ "${confirm}" = "Y" ]; then
        sudo ${last_cmd}
    fi
}
fi

function __keychain() {
    which keychain > /dev/null 2>&1
    if [ "$?" = "0" ]; then
        eval $(keychain --systemd --quiet --eval --ignore-missing --agents ssh ${_BP_KEYCHAIN_KEYS:-"id_ecdsa"} --noask --timeout 600)
    fi
}

function __settitle() {
    local cur_cmd="${@}"
    local cmd="$(hostname) | ${@}"
    if [ "${cur_cmd}" = "__prompt_command" ]; then
        cmd="$(hostname) | bash"
    fi
    echo -ne "\033]0;${cmd}\007"
}

function __pyvenv() {
    if [ ! -z "${VIRTUAL_ENV}" ]; then
        echo -n "(py:$(basename ${VIRTUAL_ENV})) "
    fi
}

function __customenv() {
    if [ ! -z "${PB_CUSTOM_ENV}" ]; then
        echo -n "(${PB_CUSTOM_ENV}) "
    fi
}

function venv_enter() {
    if [ ! -z "$1" ]; then
        venv_version=""
        if [ ! -z "$2" ]; then
            venv_version="${2}"
        fi
        if [ ! -f ~/doc/pyvenv/${1}/bin/activate ]; then
            virtualenv${venv_version} ~/doc/pyvenv/${1}/
        fi
        source ~/doc/pyvenv/${1}/bin/activate
    fi
}

function drop_caches() {
    sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
}

function git-push-all() {
    local ref=$(git branch --format '%(refname)')
    local branch=${ref#refs/heads/}
    for remote in $(git remote -v | grep '(push)$' | awk '{print $1}' | sort | uniq); do
        echo "=> push ${remote}"
        git push ${remote} ${branch}
    done
}

function git-update-merge() {
    if [ "${1}" = "" ]; then
        echo "missing parameter: origin name"
        return
    fi

    if [ "${2}" = "" ]; then
        echo "missing parameter: source branch name"
        return
    fi

    local origin=${1}
    local branch=${2}
    git fetch ${origin} ${branch}:${branch} && git merge ${branch}
}

function git-commit-interactive() {
    local resultvar=$1

    local commit_types=()
    commit_types+=('fix')
    commit_types+=('feat')
    commit_types+=('docs')
    commit_types+=('refactor')
    commit_types+=('test')

    local i=0
    for ct in "${commit_types[@]}"; do
        echo "[${i}] ${ct}"
        i=$((i+1))
    done
    read -p "Choose commit type: " commit_type

    local commit_string="${commit_types[$commit_type]}"

    read -p "Choose scope (enter if none): " commit_scope

    if [ ! "${commit_scope}" = "" ]; then
        commit_string="${commit_string}(${commit_scope})"
    fi

    read -p "Commit: " commit_msg

    commit_string="${commit_string}: ${commit_msg}"

    eval $resultvar="'${commit_string}'"
}

function docker-ip() {
    docker inspect $(docker ps|grep $1|awk '{print $1}')|grep -E '"IPAddress": "[0-9\.]+'|sed -r 's/.*"([0-9\.]+)".*/\1/g'
}

function docker-clean() {
    docker rm -f $(docker ps -aq)
    docker image prune -f
}

function docker-clean-cano() {
    docker rmi -f $(docker images|grep -E "(canopsis|none)"|grep -vE "influx|rabbit|mongo"|awk '{print $3}')
}

function gitco() {
    git-commit-interactive cs
    read -p "Final commit: ${cs}"
    git commit $* -m "${cs}"
}

function enter-netns() {
    if [ -z "${1}" ]; then
        echo -e "missing netns name:\n$(ip netns list)"
        return
    fi
    local netns="${1}"
    sudo ip netns exec ${netns} /bin/bash -l -c "su - wrk"
}

function lxc-ip() {
    if [ -z "${1}" ]; then
        echo -e "missing container name:\n$(sudo lxc-ls --active)"
        return
    fi
    sudo lxc-attach -n $1 --clear-env -- ip a
}

function lxc-bash() {
    if [ -z "${1}" ]; then
        echo -e "missing container name:\n$(sudo lxc-ls --active)"
        return
    fi
    sudo lxc-attach -n $1 --clear-env --set-var HOME=/root --set-var TERM=xterm -- /bin/bash -l
}

function cps-restore() {
    mongorestore -h $1 -u cpsmongo -p canopsis --db canopsis --authenticationDatabase=canopsis --gzip --archive=$(readlink -e "${2}") --drop
}

function cps-dump() {
    mongodump -h $1 -u cpsmongo -p canopsis --db canopsis --authenticationDatabase=canopsis --gzip --archive="${2}"
}

# aliases
if [ "${_INTERACTIVE}" = "1" ]; then
    alias vim="nvim"
    alias ovim="/usr/bin/vim"
    alias cvim="venv_enter cano && vim"
    alias dk="docker-compose"
    alias sssh="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    alias ls="ls -F --color=always --group-directories-first"
    alias l="ls"
    alias ll="ls -l"
    alias lla="ls -la"
    if (($(id -u) == 0)); then
        alias rm="rm -i"
        alias rr="rm -ri"
    else
        alias rr="rm -rf"
    fi
    alias ts="tmux list-sessions"
    alias ta="tmux attach"
    alias mpvp='ls|sort -g|sed -r "s/(.*)/\"\1\"/g"|xargs mpv'
    alias mpva='mpv --no-video'
    alias kcadd="keychain ${_BP_KEYCHAIN_KEYS:-'id_ecdsa'}"
    alias kcc="keychain --clear"
    alias kcclean="ssh-add -D"
    alias updatenow="trizen -Syu"
    alias gitcod="git commit -am '(づ ￣ ³￣)づ'"
    alias grep="grep --color=auto"
    alias gr="grep -rnI"
    alias a="setxkbmap fr bepo"
    alias doc="docker-compose"
    function go-build-static() {
        CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' $*
    }
fi

# prompt
function __prompt_command() {
    local rc="$?"
    if [ "${_INTERACTIVE}" = "1" ]; then
        local usr_color=${bldblu}
        local usr_txt='\u@\h'
        if [ $(id -u) = 0 ]; then
            usr_color=${bldred}
            usr_txt='\h'
        fi

        local rctxt=""
        if [ ! "${rc}" = "0" ]; then
            rctxt="${txtred}♥ ${rc} "
        fi

        local arrow="\xe2\x9d\xad"
        if [ "${_BP_TERM_UTF8}" = "0" ]; then
            arrow=">"
        fi

        export PS1=$(echo -e "$(__customenv)$(__pyvenv)${usr_color}${usr_txt}${bldwht} ${txtwht}$(__tmux_ps1)${bldwht}$(__netns_ps1)${rctxt}${txtwht}$(__git_ps1)${bldgrn}\w${bldwht}\n${arrow}${txtrst} ")
    else
        PS1="$ "
    fi
    history -a ${HISTFILE}
}

# environment
if [ "${_INTERACTIVE}" = "1" ]; then
    if [ "${_BP_KEYCHAIN}" = "1" ]; then
        __keychain
    fi
    if [ "${_BP_TMUX}" = "1" ]; then
        __tmux
    fi
fi

if [ "${_INTERACTIVE}" = "1" ]; then
    if [ -f /usr/share/stderred/stderred.sh ]; then
        source /usr/share/stderred/stderred.sh
    fi
fi

if [ -f ~/.cargo/env ]; then
    source ~/.cargo/env
fi

if [ "${_INTERACTIVE}" = "1" ]; then
    trap '__settitle "${BASH_COMMAND}"' DEBUG
fi

if [ -f ~/.bashrc_local ]; then
    source ~/.bashrc_local
fi
