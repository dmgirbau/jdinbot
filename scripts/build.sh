#!/bin/bash
MODE=${1:-dev}

if [ "$MODE" == "dev" ]; then
    echo "Starting dev container..."
    export DEV_MODE=true
    export ENV=development
    docker-compose up --build
elif [ "$MODE" == "prod" ]; then
    echo "Starting production container..."
    export DEV_MODE=false
    export ENV=production
    docker-compose up --build
else
    echo "Usage: $0 [dev|prod]"
    exit 1
fi