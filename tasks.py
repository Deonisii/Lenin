import os
import signal
from invoke import task

__path, _ = os.path.split(__file__)
PATH_TO_PID_FILE = os.path.join(__path, '.pid')

@task
def build(ctx):
    print('Building...')


@task(help={'name': "Name of the person to say hi to."})
def hi(_, name):
    """Say hi to someone."""
    print("Hi %s!" % name)

@task
def start_bot(ctx):
    print('start bot...')
    ctx.run(r'start "" python main.py')

@task
def stop_bot(_):
    if os.path.exists(PATH_TO_PID_FILE):
        print('stop bot...')
        pid = None
        with open(PATH_TO_PID_FILE, 'r') as f:
            pid = int(f.readline())
        if pid:
            try:
                os.kill(pid, signal.SIGABRT)
            except OSError:
                pass
        os.remove(PATH_TO_PID_FILE)

@task(pre=[stop_bot])
def upgrade_bot(ctx):
    """self upgrade from git remote repo"""
    ctx.run('git pull origin develop')
    start_bot(ctx)
