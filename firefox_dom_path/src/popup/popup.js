(function($$){
  $$.getElementById('copy').addEventListener('click', (event) => {
    navigator.clipboard.writeText(document.getElementById('json').value)
    window.close()
  })
  browser.storage.local.get('json').then((result) => {
    document.getElementById('json').value = result.json
  })
})(document)
