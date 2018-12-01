if [ -z "$GOPATH" ]; then
    export GOPATH="${HOME}/doc/go"
    export PATH="${PATH}:${GOPATH}/bin"
fi

export XKB_DEFAULT_LAYOUT=fr
export XKB_DEFAULT_VARIANT=bepo

export PATH="$HOME/.cargo/bin:$PATH"
source ~/.cargo/env
