#!/usr/bin/env sh
# simple entrypoint: propagate signals and run the command

set -e

# if mounted volume changed ownership, ensure /app is writable by the runtime user
APP_UID=${APP_UID:-1001}
APP_GID=${APP_GID:-1001}

if [ "$(id -u)" = "0" ]; then
  chown -R ${APP_UID}:${APP_GID} /app || true
  # exec is used for signal handling
  exec su-exec ${APP_USER} "$@"
fi

exec "$@"