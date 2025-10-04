#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -o errexit
# Return the exit code of the last command in the pipe that failed
set -o pipefail
# Treat unset variables as an error
set -o nounset
# Print each command before executing it (debug)
set -o xtrace

# Go to the frontend project directory inside the container
cd /app

# Start Vite development server with host binding for container access
npm run dev -- --host
