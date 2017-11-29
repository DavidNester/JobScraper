import time
from urllib import robotparser
from keywords_pseudo import *
from urllib.parse import urlparse
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import url


def get_domain(url):
    """
    gets domain of URL
    :param url: string url that we want to get domain from
    :return: domain of url
    """
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain


class Domain:
    def __init__(self, domain):
        self.domain = domain  # The domain address (facebook.com)
        self.time = time.time()
        self.keywords = []  # list of strings
        self.urls_to_visit = []
        self.urls_visited = set()
        self.rp = robotparser.RobotFileParser()
        # What happens if no robots.txt is found?
        self.rp.set_url(domain + "/robots.txt")
        self.rp.read()
        self.wait_time = self.rp.crawl_delay("*")
        if self.wait_time is None:
            self.wait_time = 0

    def add_address(self, url):
        '''
        Checks if a url of the domain can be added to
        the list of urls to visit.
        param address: the new address to be added
        :return: true if the address is in the domain.
        '''
        if get_domain(url) != self.domain:
            return False
        elif url in self.urls_visited:
            return True
        elif url in self.urls_to_visit:
            return True
        else:
            self.urls_to_visit.append(url)
        return True

    def visit_urls(self, keywords):
        relevant_urls = []
        while len(self.urls_to_visit) > 0:
            url = self.urls_to_visit.pop(0)
            keywords_found, new_urls = keywords_search(url,keywords)
            self.urls_visited.append(url)
            if keywords_found:
                relevant_urls.append(url)
            for nurl in new_urls:
                if nurl not in self.urls_visited:
                    self.urls_to_visit.append(nurl)
        return relevant_urls

    def __eq__(self, other):
        return self.domain == other.domain

    def has_next_url(self):
        '''
        Check URL to make sure that it meets all of the criteria. Not already visited,
        not .js or .php, and met domain wait time.
        return: True if the site is valid, False otherwise
        '''
        address = self.urls_to_visit.pop(0)
        if not(self.can_visit(address)):
            return False
        not_accepted = ['.js','.php']
        if not_accepted in address:
            return False
        elif address in self.urls_visited:
            return False
        while (time.time() - self.time) <= self.wait_time:
            print('Waiting ', self.wait_time - (time.time() - self.time), ' seconds for', address)
            time.sleep(self.wait_time - (time.time() - self.time()))
        return True

    def can_visit(self, url):
        if self.rp.canfetch("*", url.address):
            return True
        return False

