browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureElement") {
        let fullPath = message.path;
        let name = message.name;
        let price = message.price;
        let image = message.image;

        // Instead of opening the popup, handle or save this data
        console.log("Captured DOM Path:", fullPath);
        console.log("Name:", name);
        console.log("Price:", price);
        console.log("Image:", image);

        // Example: Save the selected attribute to storage or send to a backend
        saveToStorage(fullPath, name, price, image);
    }
});

function saveToStorage(path, name, price, image) {
    // Example of saving it to local storage
    browser.storage.local.set({ path, name, price, image }, () => {
        console.log("saved to storage", path, name, price, image);
    });
}
