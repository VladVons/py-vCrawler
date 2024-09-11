document.addEventListener('click', function(event) {
    if (event.ctrlKey) {
        let element = event.target;
        let fullPath = getDomPath(element);

        // Send the element details to the background script
        browser.runtime.sendMessage({
            action: "captureElement",
            path: fullPath,
            name: element.getAttribute('name') || 'N/A',
            price: element.getAttribute('price') || 'N/A',
            image: element.src || 'N/A'
        });
    }
});

function getDomPath(el) {
    let path = [];
    while (el) {
        let selector = el.nodeName.toLowerCase();
        if (el.id) {
            selector += `#${el.id}`;
        } else if (el.className) {
            selector += `.${el.className.trim().replace(/\s+/g, '.')}`;
        }
        path.unshift(selector);
        el = el.parentElement;
    }
    return path.join(' > ');
}
