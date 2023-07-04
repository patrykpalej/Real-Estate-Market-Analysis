class ScrapingReport:
    def __init__(self):
        self.scraping_started = None
        self.scraping_ended = None


class SearchScrapingReport(ScrapingReport):
    def __init__(self):
        super().__init__()
        self.n_of_urls_aquired_from_pages = []


class OffersScrapingReport(ScrapingReport):
    def __init__(self):
        super().__init__()
        self.n_of_offers_scraped_before = 0
        self.n_of_unknown_errors = 0
        self.n_of_offers_in_packages_attempted = []
        self.n_of_offers_in_packages_success = []

    @property
    def total_n_of_offers_attempted(self):
        return sum(self.n_of_offers_in_packages_attempted)

    @property
    def total_n_of_offers_success(self):
        return sum(self.n_of_offers_in_packages_success)
