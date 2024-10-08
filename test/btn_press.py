from playwright.sync_api import sync_playwright

ContextOpt = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "locale": "uk-UA",
    "extra_http_headers": {
        "Accept-Language": "uk-UA"
    }
}


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(**ContextOpt)
    page = context.new_page()

    # Navigate to the webpage
    Responce = page.goto('https://server-shop.ua/ua/pc/', wait_until="domcontentloaded", timeout=10000)

    while True:
        try:
            Content = page.content()
            Len = len(Content)
            print('len', Len)

            button = page.locator('button.btn_more')
            if button.is_visible():
                button.click()
                # Optionally wait for new products to load
                page.wait_for_timeout(3000)  # Adjust the timeout as necessary
            else:
                # Break the loop if the button does not exist
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # After loading all products, you can process them as needed
    products = page.query_selector_all('.product-item')

    browser.close()

