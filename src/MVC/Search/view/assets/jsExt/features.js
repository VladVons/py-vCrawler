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
  }

  ScriptTest() {
    const Script = this.ElScript.value.trim();
    this.ElResult.value = '';

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

    const FileData = atob(res['data']);
    const data = new Blob([FileData], { type: 'application/vnd.ms-excel' });
    const downloadUrl = URL.createObjectURL(data);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = "findwares_p.xlsx";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(downloadUrl);

    this.Log(res['err']);
  }

  LoadRandom() {
    const res = new TSend().exec(
      '/api/?route=scheme/features',
      {
        'method': 'LoadRandom',
        'param': {}
      }
    )

    this.ElScript.value = res['data'];
    this.Log(res['err']);
  }

  Log(Msg) {
    this.LogCnt++;
    const Now = getCurrentDateTimeString();
    this.ElLog.value += `${this.LogCnt}, ${Now}\n${Msg}\n`;
    this.ElLog.scrollTop = this.ElLog.scrollHeight;
  }
}

