import requests

from .exceptions import NASAResponseError


def handle_response(response):
    """
    Catches non-200 responses and raises, or returns the response.
    :return: response
    """
    if response.status_code != 200:
        raise NASAResponseError(response.content)
    else:
        return response


def handle_search_response(response):
    """
    Wraps handle_response and initializes a NASAResponse object.
    :param response: 
    :return: NASAResponse
    """
    response = handle_response(response)
    return NASAResponse(response)


class NASAResponse(object):

    def __init__(self, raw_response):
        data = raw_response.json()['collection']
        self.items = data['items']
        self.next_link = None
        self.previous_link = None
        links = data['links']
        # This assumes theres only one of each and Im ok with this
        for link in links:
            if link['rel'] == 'next':
                self.next_link = link['href']
            elif link['rel'] == 'prev':
                self.previous_link = link['href']

    def fetch_next(self):
        if self.next_link:
            response = requests.get(self.next_link)
            return handle_search_response(response)

    def fetch_previous(self):
        if self.next_link:
            response = requests.get(self.next_link)
            return handle_search_response(response)
