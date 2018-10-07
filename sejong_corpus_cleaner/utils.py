import subprocess

def check_encoding(paths):
    for path in paths:
        print(subprocess.getstatusoutput("file %s" % path)[1])