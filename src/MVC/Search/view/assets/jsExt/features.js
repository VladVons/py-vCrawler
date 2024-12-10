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
    document.querySelector('.idBtnRnd').onclick = (event) => {
      this.LoadRandom();
    }
    document.querySelector('.idBtnExcel').onclick = (event) => {
      this.AsExcel();
    }
    document.querySelector('.idBtnDbRefresh').onclick = (event) => {
      this.DbRefresh();
    }
  }

  ScriptTest() {
    const Script = this.ElScript.value.trim();

    // redraw
    this.ElResult.value = '';
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

      this.ElResult.value = res['data'];
      this.Log(res['err']);
    }, 0.1);
  }

  AsExcel() {
    const Script = this.ElScript.value.trim();

    this.ElResult.value = '';
    const res = new TSend().exec(
      '/api/?route=scheme/features',
      {
        'method': 'AsExcel',
        'param': {
          'aScript': Script
        }
      }
    )

    const byteArray = Base64ToBin(res['data']);
    const data = new Blob([byteArray], { type: 'application/vnd.ms-excel' });
    ExecDownload("findwares_p.xlsx", data)

    this.Log(res['err']);
  }

  LoadRandom() {
    // redraw
    this.ElScript.value = '';
    setTimeout(() => {
      const res = new TSend().exec(
        '/api/?route=scheme/features',
        {
          'method': 'LoadRandom',
          'param': {}
        }
      )

      this.ElScript.value = res['data'];
      this.Log(res['err']);
    }, 0.1);
  }

  DbRefresh() {
    this.Log('wait ...');
    // redraw
    setTimeout(() => {
      const res = new TSend().exec(
        '/api/?route=scheme/features',
        {
          'method': 'ProductsNoAttrRefresh',
          'param': {}
        }
      )

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
