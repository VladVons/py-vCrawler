# Created: 2025.05.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Var.Dict import DeepGetByList

async def Main(aData: dict, aSession):
    CountryId = DeepGetByList(aData, ['param', 'aQuery', 'country_id'])
    if (CountryId):
        aData['session']['country_id'] = CountryId
        aSession.Set('country_id', CountryId)
