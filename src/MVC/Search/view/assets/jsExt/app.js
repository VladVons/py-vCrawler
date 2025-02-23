function btnClear(aKey) {
    document.getElementById('viBtn_Clear').addEventListener('click', function (event) {
        LStorage = new TLocalStorage('products_' + aKey)
        LStorage.remove()
        document.getElementById('viCount_' + aKey).innerHTML = null
        document.getElementById('viForm_' + aKey).innerHTML = null
    })
}