from app.scraper import scrape_wikipedia

url = "https://en.wikipedia.org/wiki/China"
data = scrape_wikipedia(url)

print("TITLE:")
print(data["title"])
print("\nCONTENT PREVIEW (first 500 chars):")
print(data["content"][:500])
