import requests

from .exceptions import NASAValidationError
from .response import handle_response

API_ROOT = 'https://images-api.nasa.gov'
SEARCH_ENDPOINT = '{}/{}'.format(API_ROOT, 'search')

MEDIA_AUDIO = 'audio'
MEDIA_IMAGE = 'image'
MEDIA_VIDEO = 'video'
VALID_MEDIA_TYPES = [MEDIA_AUDIO, MEDIA_IMAGE, MEDIA_VIDEO]


def validate_media_type(value):
    if value is not None and value not in VALID_MEDIA_TYPES:
        raise NASAValidationError('{} is not a valid media type'.format(value))
    return value


def validate_year(value):
    """
    Check 4 digit year.
    :param value: 
    :return: Validated 4 digit year, or None if value was None. Raises otherwise.
    """
    # Dont want any logic in search: if this is None just pass it back
    if value is None:
        return

    value = int(value)
    if 999 < value < 10000:
        return value
    else:
        raise NASAValidationError('{} is not a valid 4 digit year.')


def _serialize_optional_list_param(value, opt_validator=lambda v: v):
    """
    
    :param value: 
    :param opt_validator: Function to validate the value. Should return the value or raise. 
    :return: 
    """
    if type(value) == list:
        # join if its a list
        value = ','.join(opt_validator(v) for v in value)
    # If not a list, ship it if its valid.
    return opt_validator(value)


def search(query=None, description=None, center=None, keywords=None, location=None, media_type=None,
           nasa_id=None, photographer=None, secondary_creator=None, title=None, year_start=None, year_end=None):
    """
    All parameters are optional, but at least one must be passed.
    
    :param query:  Text search of all fields.
    :param description: Description of the resource.
    :param center: NASA center which published the resource
    :param keywords: Keyword/tags. Can pass multiple as a list.
    :param location: Location.
    :param media_type: Must be one of VALID_MEDIA_TYPES. Can pass multiple as a list.
    :param nasa_id: Nasa resource identifier.
    :param photographer: Name of the photographer.
    :param secondary_creator: Name of the secondary photographer.
    :param title: Resource title.
    :param year_start: 4 digit year YYYY. Provides lower bound.
    :param year_end: 4 digit year YYYY. Provides upper bound.
    :return: 
    """
    keywords = _serialize_optional_list_param(keywords)
    media_type = _serialize_optional_list_param(media_type, validate_media_type)
    year_start = validate_year(year_start)
    year_end = validate_year(year_end)
    response = requests.get(SEARCH_ENDPOINT, {'q': query,
                                              'center': center,
                                              'description': description,
                                              'keywords': keywords,
                                              'location': location,
                                              'media_type': media_type,
                                              'nasa_id': nasa_id,
                                              'photographer': photographer,
                                              'secondary_creator': secondary_creator,
                                              'title': title,
                                              'year_start': year_start,
                                              'year_end': year_end})

    return handle_response(response)


