# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.PluginApp import TPluginApp
from Task import App


class TMain():
    async def Run(self, aParam: dict = None):
        Plugin = TPluginApp(App.DirConf)
        Plugin.Init('Task.Service.SchemeTest', 'Task.Service.0_Plugin')
        if (isinstance(aParam, dict)):
            for Key, Val in aParam.items():
                Plugin.ConfEx[Key] = Val
        await Plugin.Run()
