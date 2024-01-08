#!/bin/bash

# Check Python version and start a server accordingly
if command -v python2 &>/dev/null; then
    python2 -m SimpleHTTPServer
elif command -v python3 &>/dev/null; then
    python3 -m http.server
else
    echo "Python is not installed. Cannot start the server."
fi
