from discogs import scraper

scraper = scraper.DiscogsMarketplaceScraper(22835513, 5)
df = scraper.fetch_items