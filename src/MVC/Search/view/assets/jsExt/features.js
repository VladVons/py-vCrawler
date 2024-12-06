// Created: 2024.12.06
// Author: Vladimir Vons <VladVons@gmail.com>
// License: GNU, see LICENSE for more details


class TFeatures {
  constructor() {
    this.LogCnt = 0;

    this.ElScript = document.querySelector('.idTaScript');
    this.ElResult = document.querySelector('.idTaResult');
    this.ElLog = document.querySelector('.idTaLog');

    document.querySelector('.idBtnTest').onclick = (event) => {
      this.ScriptTest();
    }
  }

  ScriptTest() {
    const Script = this.ElScript.value.trim();
    this.ElResult.value = '';

    this.Log('Sending request...')
    // allow redraw
    setTimeout(() => {
      const res = new TSend().exec(
        '/api/?route=scheme/features',
        {
          'method': 'ScriptTest',
          'param': {
            'aScript': Script
          }
        }
      )

      this.ElResult.value = res['data'] || '';
      this.Log(res['err']);
    }, 0.1);
  }

  Log(Msg) {
    this.LogCnt++;
    const Now = getCurrentDateTimeString();
    this.ElLog.value += `${this.LogCnt}, ${Now}\n${Msg}\n`;
    this.ElLog.scrollTop = this.ElLog.scrollHeight;
  }
}

