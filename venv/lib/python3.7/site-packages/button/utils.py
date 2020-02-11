import shlex, subprocess
import time

def execute_shell_command(command, preserve_output=False):
    lines = []
    cmd = "sh -c '{}'".format(command)
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        line_utf8 = line.decode('utf-8').rstrip()
        print(line_utf8)
        if preserve_output:
            lines.append(line_utf8)
    retval = p.poll()
    return retval, lines
