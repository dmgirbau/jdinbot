#!/usr/bin/env sh
# simple entrypoint: propagate signals and run the command
set -e

# if mounted volume changed ownership, ensure /app is writable by the runtime user
if [ "$(id -u)" = "0" ]; then
  chown -R $(id -u ${APP_USER} 2>/dev/null || echo 1001):$(id -g ${APP_USER} 2>/dev/null || echo 1001) /app || true
  exec su-exec ${APP_USER} "$@"
fi

exec "$@"