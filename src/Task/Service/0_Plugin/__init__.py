# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList, TDbCond

def SiteCondEnabled(aDbl: TDbList) -> TDbList:
    Cond = TDbCond().AddFields([
        ['eq', (aDbl, 'enable'), 1]
    ])
    return aDbl.Clone(aCond=Cond)
