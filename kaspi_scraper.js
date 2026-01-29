const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

const fs = require('fs');
const path = require('path');

const PRODUCTS_FILE = path.join(__dirname, 'products.json');
const OUTPUT_FILE = path.join(__dirname, 'kaspi_prices.json');

async function scrape() {
    const products = JSON.parse(fs.readFileSync(PRODUCTS_FILE, 'utf-8'));
    console.log(`Starting scraper for ${products.length} products...`);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    const results = [];

    for (let i = 0; i < products.length; i++) {
        const query = products[i];
        console.log(`[${i + 1}/${products.length}] Searching for: ${query}`);

        try {
            // Navigate to search
            const searchUrl = `https://kaspi.kz/shop/search/?text=${encodeURIComponent(query)}`;
            await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 30000 });

            // Check if there are results
            const firstCard = await page.locator('.item-card').first();
            const exists = await firstCard.isVisible();

            if (exists) {
                const title = await firstCard.locator('.item-card__name').innerText();
                const priceText = await firstCard.locator('.item-card__prices-price').first().innerText();
                const productUrl = await firstCard.locator('.item-card__name-link').getAttribute('href');

                let sellers = "1"; // Default
                let apiSellersCount = 0;

                // Setup listener for this specific page load
                const ResponsePromise = page.waitForResponse(response =>
                    response.url().includes('/offer-view/offers/') &&
                    response.status() === 200 &&
                    !response.url().endsWith('/offers') // Avoid the generic empty one if any
                    , { timeout: 10000 }).catch(() => null);

                try {
                    console.log(`Navigating to product page: https://kaspi.kz${productUrl}`);
                    await page.goto(`https://kaspi.kz${productUrl}`, { waitUntil: 'domcontentloaded', timeout: 30000 });

                    const response = await ResponsePromise;
                    if (response) {
                        try {
                            const json = await response.json();
                            if (json && json.offers) {
                                // Prefer the explicit total count from the API
                                if (json.offersCount) {
                                    apiSellersCount = json.offersCount;
                                } else if (json.total) {
                                    apiSellersCount = json.total;
                                } else {
                                    apiSellersCount = json.offers.length;
                                }

                                console.log(`[API] Intercepted data. Total Offers: ${apiSellersCount}`);
                                sellers = apiSellersCount.toString();
                            }
                        } catch (jsonErr) {
                            console.log("Error parsing API json:", jsonErr.message);
                        }
                    } else {
                        console.log("API response timeout or not found, falling back to DOM");
                        // Fallback to DOM (Offers tab text)
                        try {
                            const offersTab = page.locator('li[data-tab="offers"]');
                            if (await offersTab.isVisible()) {
                                const text = await offersTab.innerText();
                                const match = text.match(/\((\d+)\)/);
                                if (match) sellers = match[1];
                            }
                        } catch (e) { }
                    }

                } catch (e) {
                    console.error(`Error on product page:`, e.message);
                }

                results.push({
                    query,
                    match: title,
                    price: priceText.replace(/\s/g, '').replace('₸', ''),
                    sellers: sellers,
                    url: productUrl
                });
                console.log(`Found: ${title} - ${priceText} (${sellers} sellers)`);
            } else {
                console.log(`No results for: ${query}`);
                results.push({ query, match: null, price: null, sellers: null });
            }

            // Small random delay to be less bot-like
            await page.waitForTimeout(Math.floor(Math.random() * 2000) + 1000);

        } catch (error) {
            console.error(`Error searching for ${query}:`, error.message);
            results.push({ query, error: error.message });
        }
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));
    console.log(`Scraping completed. Results saved to ${OUTPUT_FILE}`);

    await browser.close();
}

scrape();
