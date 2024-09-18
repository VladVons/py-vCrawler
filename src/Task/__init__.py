# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import argparse
#
from Inc.Conf import TConf
from Inc.ConfJson import TConfJson
from Inc.PluginTask import TPluginTask
from Inc.Misc.Log import TEchoConsoleEx, TEchoFileEx
from Inc.Misc.Env import GetEnvWithWarn
from IncP.Log import Log
from IncP import GetInfo


def LoadClassConf(aClass: object) -> dict:
    File = f'{DirConf}/{aClass.__module__}.json'
    try:
        Res = TConfJson().LoadFile(File)
    except Exception as E:
        Log.Print(1, 'e', f'{E} in {File}')
        raise
    return Res

def _InitOptions():
    Usage = f'usage: {AppName} [options] arg'
    Parser = argparse.ArgumentParser(usage = Usage)
    Parser.add_argument('-c', '--conf',     help='config',            default='Default')
    Parser.add_argument('-i', '--info',     help='information',       action='store_true')
    return Parser.parse_args()

def _InitLog():
    FileLog = f'/var/log/{AppName}/{AppName}.log'
    if (not os.path.exists(FileLog)) or (not os.access(FileLog, os.W_OK)):
        FileLog = sys.argv[0].removesuffix('.py') + '.log'
    Log.AddEcho(TEchoFileEx(FileLog))
    print(f'Log file {FileLog}')

    Log.AddEcho(TEchoConsoleEx())

AppName = GetInfo()['app_name']
Options = _InitOptions()
_InitLog()

DirConf = f'Conf/{Options.conf}'
ConfTask = TConf(f'{DirConf}/Task.py')
ConfTask.Load()
Plugin = TPluginTask('Task', DirConf)
