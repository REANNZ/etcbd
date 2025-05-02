#!/bin/bash

# Propagate script errors
set -eu

# Exec all scripts from /etc/startup.d
STARTUP_DIR=/etc/startup.d
if [ -d "$STARTUP_DIR" ] ; then
    for STARTUP_FILE in $STARTUP_DIR/*.sh ; do
        if [ -x "$STARTUP_FILE" ]; then
            $STARTUP_FILE
        fi
    done
fi

exec "$@"


