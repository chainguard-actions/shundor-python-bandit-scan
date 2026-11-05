import subprocess


def run(cmd):
    subprocess.call(cmd, shell=True)


def check(x):
    assert x > 0
    return x
