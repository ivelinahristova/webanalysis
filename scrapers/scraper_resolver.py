from scrapers.scraper_strategies.bivol_strategy import BivolStrategy
from scrapers.scraper_strategies.dariknews_strategy import DariknewsStrategy
from scrapers.scraper_strategies.dnevnik_strategy import DnevnikStrategy
from scrapers.scraper_strategies.vesti_strategy import VestiStrategy


class ScraperResolver:
    __strategies = {}

    def __init__(self):
        strategy = DnevnikStrategy()
        self.__strategies[strategy.get_name()] = strategy
        strategy_dariknews = DariknewsStrategy()
        self.__strategies[strategy_dariknews.get_name()] = strategy_dariknews
        strategy_vesti = VestiStrategy()
        self.__strategies[strategy_vesti.get_name()] = strategy_vesti
        strategy_bivol = BivolStrategy()
        self.__strategies[strategy_bivol.get_name()] = strategy_bivol

    def get_strategy(self, source):
        return self.__strategies[source]

    def get_all(self):
        return self.__strategies

