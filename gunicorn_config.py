# Gunicorn configuration file for MechLocator
# Run with: gunicorn -c gunicorn_config.py mechlocator.wsgi:application

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:10000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "mechlocator"

# Server mechanics
daemon = False
pidfile = "/tmp/mechlocator.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=mechlocator.settings",
    "DEBUG=False",
    "ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1,*",
]

# Pre-fork application loading
def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_request(worker, req):
    worker.log.info("%s %s" % (req.method, req.path))

def post_request(worker, req, environ, resp):
    worker.log.info("%s %s - %s" % (req.method, req.path, resp.status))
