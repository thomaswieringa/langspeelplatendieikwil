from scraper.discog.discogs_versions import Versions
from watchlist_manager import WatchlistManager

versions = Versions(key="IjDxhwugeqUVGtMZuJZQqCazFHdMQXKrZOTesFTj",
                                     user="thomaswieringa")

watchlist_manager = WatchlistManager(key="IjDxhwugeqUVGtMZuJZQqCazFHdMQXKrZOTesFTj", versions=versions)
watchlist_manager.run()
