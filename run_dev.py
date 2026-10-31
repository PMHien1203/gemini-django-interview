#!/usr/bin/env python3
import sys
import os

if __name__ == '__main__':
    host = '0.0.0.0'
    port = '3000'
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == '--host' and i + 1 < len(args):
            host = args[i + 1]
        elif arg.startswith('--host='):
            host = arg.split('=', 1)[1]
        elif arg == '--port' and i + 1 < len(args):
            port = args[i + 1]
        elif arg.startswith('--port='):
            port = arg.split('=', 1)[1]

    addr = f"{host}:{port}"
    print(f"Starting Django development server on {addr}...", flush=True)
    os.execlp("python3", "python3", "manage.py", "runserver", addr)
