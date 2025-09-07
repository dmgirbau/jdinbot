#!/usr/bin/env sh
# simple entrypoint: propagate signals and run the command

set -e
for var in POSTGRES_HOST POSTGRES_PORT POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB; do
  if [ -z "${!var}" ]; then
    echo "Error: $var is not set"
    exit 1
  fi
done

# if mounted volume changed ownership, ensure /app is writable by the runtime user
APP_UID=${APP_UID:-1001}
APP_GID=${APP_GID:-1001}

if [ "$(id -u)" = "0" ]; then
  chown -R ${APP_UID}:${APP_GID} /app || true
  # exec is used for signal handling
  exec gosu ${APP_USER} "$@"
fi

exec "$@"