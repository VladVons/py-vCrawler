const elScript = document.getElementById('ta_script')
const elResult = document.getElementById('ta_result')
const elError = document.getElementById('ta_error')
const elHelp = document.getElementById('ta_help')

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

document.getElementById('btn_test').onclick = function(event) {
  const Script = elScript.value.trim()
  if (Script != '') {
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'Parse',
        'param': {
          'aScript': Script
        }
      }
    )

    elError.value = res['err']
    elResult.value = res['data'] || ''
  } else {
    elError.value = 'empty script'
  }
}

function HandleDblClickErr() {
  elError.addEventListener('dblclick', (event) => {
    const ErrText = GetCurLineText(event.target)
    const Script = elScript.value.trim()
    const res = new TSend().exec(
      '/api/?route=scheme/test',
      {
        'method': 'GetLineNo',
        'param': {
          'aScript': Script,
          'aErr': ErrText
        }
      }
    )

    if (res['line'] >= 0) {
      moveCursorToLine(elScript, res['line'], res['column']);
    }
  });
};

function TextNumbering() {
  function AddNumbering(aTextArea, aNumbers) {
    const num = aTextArea.value.split('\n').length + 1;
    aNumbers.innerHTML = Array(num).fill('<span></span>').join('');
  }

  const editors = document.querySelectorAll('.editor');
  for (const editor of editors) {
    const textarea = editor.querySelector('textarea');
    const numbers = editor.querySelector('.numbers');
    AddNumbering(textarea, numbers)

    textarea.addEventListener('keyup', (e) => {
      AddNumbering(textarea, numbers)
    });
  }
}

function TabChange(aTarget) {
  aTarget.addEventListener('shown.bs.tab', function(event) {
    const currentTab = event.target;
    if (currentTab.id === 'tab-help') {
      const res = new TSend().exec(
        '/api/?route=scheme/test',
        {
          'method': 'GetHelp',
          'param': {
            'aScript': elScript.value.trim()
          }
        }
      )
      elHelp.value = res['help']
    }
  });
}