# DVRPC, W?T, 02-Apr-2019

import os
import subprocess
import sys
import time

MESSAGEPRIORITY_NOTE    = 0b0101<<12
MESSAGEPRIORITY_ERROR   = 0b0011<<12
WRITE_TO_CONSOLE = False

class _Visum:
    # Dummy debug class
    VersionNumber = "1800"
    @classmethod
    def Log(cls, priority, msg):
        print msg
    @classmethod
    def WriteToTrace(cls, msg):
        print msg

def WriteToTrace(Visum, msg, *args, **kwds):
    Visum = _Visum if Visum is None else Visum
    if (int(Visum.VersionNumber[:2]) > 15):
        Visum.Log(MESSAGEPRIORITY_NOTE, msg)
    else:
        Visum.WriteToTrace(msg)
    if WRITE_TO_CONSOLE:
        sys.stdout.write(msg)
def WriteToError(Visum, msg, *args, **kwds):
    Visum = _Visum if Visum is None else Visum
    if (int(Visum.VersionNumber[:2]) > 15):
        Visum.Log(MESSAGEPRIORITY_ERROR, msg)
    else:
        Visum.WriteToTrace(msg)
    if WRITE_TO_CONSOLE:
        sys.stdout.write(msg)

def RunExternalCmd(Visum, cmdArgs):
    WriteToTrace(
        Visum,
        "Running cmd: '%s' within: '%s'" % (
            " ".join(cmdArgs),
            os.path.abspath(os.curdir)
        )
    )
    assert os.name is "nt", "Unsupported OS: %s" % os.name
    sui = subprocess.STARTUPINFO()
    sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    pkwds = {
        'args': cmdArgs,
        'startupinfo': None if WRITE_TO_CONSOLE else sui,
        'stdout': None if WRITE_TO_CONSOLE else subprocess.PIPE,
        'stderr': None if WRITE_TO_CONSOLE else subprocess.PIPE,
        'creationflags': subprocess.CREATE_NEW_CONSOLE if WRITE_TO_CONSOLE else 0
    }
    p = subprocess.Popen(**pkwds)
    while (not WRITE_TO_CONSOLE) and p.poll() is None:
        WriteToTrace(Visum, p.stdout.readline())
    if not WRITE_TO_CONSOLE:
        stdout, stderr = p.communicate()
        if (stdout is not None) and (stdout <> ''):
            WriteToTrace(Visum, stdout)
        if (stderr is not None) and (stderr <> ''):
            WriteToError(Visum, stderr)
    else:
        p.wait()
    WriteToTrace(Visum, "Finished: %s" % " ".join(cmdArgs))

# RunExternalCmd(Visum, (r"C:\Users\wtsay\Desktop\RunCmd.bat",))