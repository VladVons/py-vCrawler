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
    let currentEl = el;

    while (currentEl && currentEl.nodeName.toLowerCase() !== 'body') {
        // Get the element name and start building the tag
        let selector = `<${currentEl.nodeName.toLowerCase()}`;

        // Append all attributes of the element exactly as they appear in the tag
        Array.from(currentEl.attributes).forEach(attr => {
            selector += ` ${attr.name}="${attr.value}"`;
        });

        // Close the tag representation
        selector += `>`;

        // Get element's index among its siblings (if it's not the only one)
        const siblings = Array.from(currentEl.parentElement ? currentEl.parentElement.children : []);
        const index = siblings.indexOf(currentEl) + 1;

        if (siblings.length > 1 && index > 0) {
            selector += `[${index}]`;
        }

        path.unshift(selector);
        currentEl = currentEl.parentElement;
    }

    return path.join(' / ');
}
