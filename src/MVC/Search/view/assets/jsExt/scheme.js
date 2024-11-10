// Created: 2024.10.31
// Author: Vladimir Vons <VladVons@gmail.com>
// License: GNU, see LICENSE for more details


function GetCurLineText(aTextArea) {
  const Lines = aTextArea.value.split('\n');
  let charCount = 0;
  for (const xLine of Lines) {
    charCount += xLine.length + 1;
    if (aTextArea.selectionStart < charCount) {
      return xLine;
    }
  }
};

function moveCursorToLine(aTextArea, aLineNo, aColumn = 0) {
  const lines = aTextArea.value.split('\n');
  if (aLineNo < 1 || aLineNo > lines.length) {
    return;
  }

  let charOffset = 0;
  let i = 0;
  for (; i < aLineNo - 1; i++) {
    charOffset += lines[i].length + 1;  // Add 1 for newline character
  }

  if (aColumn == -1) {
    aColumn = lines[i].length;
  }
  aTextArea.setSelectionRange(charOffset, charOffset + aColumn);
  aTextArea.focus();
}

function GetHelp() {
  const res = new TSend().exec(
    '/api/?route=scheme/test',
    {
      'method': 'GetHelp',
      'param': {}
    }
  )

  let Res = [];
  for (const xItem of res['help']) {
    Res.push('');
    Res.push(xItem[0].trim());
    let Parts = xItem[1].split('\n');
    for (const xPart of Parts) {
      Res.push(xPart.trim());
    }
  }

  return Res.join('\n');
}

class TScriptTest {
  constructor(aName) {
    this.Name = aName;
    this.LogCnt = 0;

    this.ElTab = document.getElementById(`tab-${aName}`);
    this.ElScript = this.ElTab.querySelector('.idTaScript');
    this.ElResult = this.ElTab.querySelector('.idTaResult');
    this.ElLog = this.ElTab.querySelector('.idTaLog');
    this.ElUrl = this.ElTab.querySelector('.idUrl');
    this.ElTestEmul = this.ElTab.querySelector('.idBtnTestEmul');
    this.ElService = document.getElementById('TaService');

    this.ElTab.querySelector('.idBtnTest').onclick = (event) => {
      this.ScriptTest();
    }

    this.ElLog.addEventListener('dblclick', (event) => {
      this.OnDblClickErr(event);
    });

    this.ElResult.addEventListener('dblclick', (event) => {
      this.OnDblClickResult(event);
    });

    this.ElScript.addEventListener('paste', (event) => {
      this.OnPasteScript(event);
    });

    this.ElTab.querySelector('.idCommands').addEventListener('change', (event) => {
        const Value = event.target.value;
        if (Value == 'TplNew') {
          this.LoadTemplate('new');
        } else if (Value == 'TplRnd') {
          this.LoadTemplate('rnd');
        } else if (Value == 'PrettySrc') {
          this.LoadPrettySrc();
        } else if (Value == 'GetMacroses') {
          this.GetMacroses();
        } else if (Value == 'LogClear') {
          this.ElLog.value = '';
        } else if (Value == 'CacheClear') {
          this.CacheClear();
        }
    });

    this.TextNumbering();
  }

  LoadTemplate(aType) {
    if ((this.ElScript.value.trim() != '') && (!confirm(`Load ${aType} ${this.Name} scheme ?`))) {
      return;
    }

    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'GetTemplate',
        'param': {
          'aName': this.Name,
          'aType': aType
        }
      }
    )

    const Script = res['script'];
    const ScriptJ = JSON.parse(Script);
    const Url = ScriptJ[this.Name]['info']['url'];
    window.open(Url, "_blank");

    this.ElScript.value = Script;
    this.ElResult.value = '';
    this.ElUrl.value = '';

    this.Log(`${aType} ${this.Name} scheme loaded`);
  }

  ScriptTest() {
    const Url = this.ElUrl.value.trim();
    if (Url == '') {
      this.Log('empty url');
      return;
    }

    const Script = this.ElScript.value.trim();
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'Parse',
        'param': {
          'aUrl': Url,
          'aScript': Script,
          'aEmul': this.ElTestEmul.checked
        }
      }
    )

    this.ElResult.value = res['data'] || '';
    this.Log(res['err']);
  }

  TextNumbering() {
    function AddNumbering(aTextArea, aNumbers) {
      const num = aTextArea.value.split('\n').length + 1;
      aNumbers.innerHTML = Array(num).fill('<span></span>').join('');
    }

    const editors = this.ElTab.querySelectorAll('.editor');
    for (const editor of editors) {
      const textarea = editor.querySelector('textarea');
      const numbers = editor.querySelector('.numbers');
      AddNumbering(textarea, numbers);

      textarea.addEventListener('keyup', (e) => {
        AddNumbering(textarea, numbers);
      });
    }
  }

  OnDblClickResult(event) {
    const CurLine = GetCurLineText(event.target);
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'GetUrlFromText',
        'param': {
          'aText': CurLine
        }
      }
    )

    if (res && res['url']) {
      window.open(res['url'], "_blank");
    }
  }

  OnDblClickErr(event) {
      const CurLine = GetCurLineText(event.target);
      const Script = this.ElScript.value.trim();
      const res = new TSend().exec(
        '/api/?route=scheme/test',
        {
          'method': 'GetLineNo',
          'param': {
            'aScript': Script,
            'aCurLine': CurLine
          }
        }
      )

      if (res['line'] >= 0) {
        moveCursorToLine(this.ElScript, res['line'], res['column']);
      }
  }

  LoadPrettySrc() {
    const Url = this.ElUrl.value.trim();
    if (Url == '') {
      this.Log('empty url');
      return;
    }

    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'GetPrettySrc',
        'param': {
          'aUrl': Url,
          'aEmul': this.ElTestEmul.checked
        }
      }
    )
    this.ElService.value = res['src'];
    this.Log('pretty source loaded into service tab');
  }

  GetMacroses() {
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'GetMacroses',
        'param': {
          'aScript': this.ElScript.value
        }
      }
    )

    const Msg = 'used macroses:\n' + `${res['macroses'].join('\n')}`
    this.Log(Msg);
  }

  CacheClear() {
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'CacheClear',
        'param': {}
      }
    )

    this.Log(`files removed: ${res['files_cnt']}`);
  }

  OnPasteScript(event) {
    const clipboardData = event.clipboardData.getData('text');
    const ScriptJ = JSON.parse(clipboardData);
    const Data = ScriptJ[this.Name]['info']['urls'];
    const Urls = Object.values(Data);
    for (const xUrl of Urls) {
      if ((xUrl) && (xUrl[0] != '-')) {
        this.ElUrl.value = xUrl;
        break;
      }
    }
  }

  Log(Msg) {
    this.LogCnt++;
    const Now = getCurrentDateTimeString();
    this.ElLog.value += `${this.LogCnt}, ${Now}\n${Msg}\n`;
    this.ElLog.scrollTop = this.ElLog.scrollHeight;
  }
}
