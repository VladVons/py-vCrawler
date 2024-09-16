// поля для заполнения
const FIELDS = ['вибери ключ зі списку:', 'name','price','description'];

(function($$){
  browser.storage.local.set({json: JSON.stringify({})}) // данные результата
  
  // обработчик события
  $$.documentElement.addEventListener('click', (event) => {
    //event.preventDefault(); // Отмена перехода по ссылке
    if(event.ctrlKey) {
      let data = []
      let node = event.target
      let x = event.clientX
      let y = event.clientY
      
      // рекурсия
      while(node != $$.documentElement) {
        let attr =  Array.from(node.attributes)
        data.push(`<${node.nodeName}` + attr.map(item => ` ${item.name}="${item.value}"`) + '>')
        node = node.parentNode
      }
      data = data.reverse() // конечная строка
      
      let select = $$.createElement('SELECT') // поле выбора
      select.setAttribute('style', `position: absolute; top: ${y}px; left: ${x}px; font-size: 20px; z-index: 999999`)
      // заполнение значениями
      for(field of FIELDS) {
        let option = $$.createElement('OPTION')
        option.textContent = field
        option.style.fontSize = '20px'
        select.appendChild(option)
      }
      $$.body.appendChild(select)
      
      // обработка выбора
      select.addEventListener('change', (event) => {
        browser.storage.local.get('json').then((result) => {
          let json = JSON.parse(result.json)
          json[event.target[event.target.selectedIndex].textContent] = data.join('')
          browser.storage.local.set({json: JSON.stringify(json)})
        })
        event.target.parentNode.removeChild(event.target)
      })
    }
  })
})(document)