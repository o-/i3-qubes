#!/bin/env python2

"""
Takes command as argument and calls that command in the currently focused vm.
Usecase:
    Use a shortcut to spawn a terminal in the same vm you are currently working
"""

import sys
import subprocess
import json

tr = subprocess.Popen(["i3-msg", "-t", "get_tree"], stdout=subprocess.PIPE).communicate()[0]
vms = subprocess.Popen(["qvm-ls", "--raw-list"], stdout=subprocess.PIPE).communicate()[0]

def focused(tree):
    if tree['focused']:
            return tree
    for t in tree['nodes']:
            f = focused(t)
            if f:
                    return f
    return None

tr = json.loads(tr)
fc = focused(tr)

vm = fc["window_properties"]["qubes_vmname"]

cmd = str(sys.argv[1])

if vm in vms:
    if vm == "dom0":
        subprocess.call([cmd])
    else:
        subprocess.call(["qvm-run", "-a", vm, cmd])
