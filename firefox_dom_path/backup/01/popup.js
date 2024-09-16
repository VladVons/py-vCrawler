document.getElementById('name').addEventListener('click', () => {
    browser.runtime.sendMessage({ action: "saveToFile", type: "name" });
});

document.getElementById('price').addEventListener('click', () => {
    browser.runtime.sendMessage({ action: "saveToFile", type: "price" });
});

document.getElementById('image').addEventListener('click', () => {
    browser.runtime.sendMessage({ action: "saveToFile", type: "image" });
});
