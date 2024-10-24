    function TextHighlightLine() {
      function highlightLine() {
        const { value, selectionStart } = textarea;
        const beforeCursor = value.substring(0, selectionStart);
        const lineIndex = beforeCursor.split('\n').length;
        const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);

        const scrollTop = textarea.scrollTop;
        const highlightPosition = lineIndex * lineHeight - scrollTop - 10;

        let highlight = document.getElementById('highlight');
        if (!highlight) {
          highlight = document.createElement('div');
          highlight.id = 'highlight';
          textarea.parentElement.appendChild(highlight);
        }

        highlight.style.top = `${highlightPosition}px`;
        highlight.style.height = `${lineHeight}px`;
      }

      const textarea = document.getElementById('ta_script')

      textarea.addEventListener('input', highlightLine);
      textarea.addEventListener('scroll', highlightLine);
      textarea.addEventListener('click', highlightLine);
      textarea.addEventListener('keyup', highlightLine);
    }
