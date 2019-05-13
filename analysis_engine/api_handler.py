# -*- coding: utf-8 -*-
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
##############################################################################

'''
Flight Data Analyzer: API Handler
'''

##############################################################################
# Imports


import abc
import logging
import numpy as np
import six

from flightdatautilities import api

from analysis_engine import library, settings


##############################################################################
# Globals


logger = logging.getLogger(name=__name__)


##############################################################################
# Classes


class MethodInterface(six.with_metaclass(abc.ABCMeta, object)):
    '''
    Abstract base class for Flight Data Analyser API handler classes.
    '''

    @abc.abstractmethod
    def get_aircraft(self, aircraft):
        '''
        Returns details of an aircraft matching the provided tail number.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: aircraft info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def get_analyser_profiles(self, aircraft):
        '''
        Returns details of analyser profiles enabled for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: analyser profiles in (module_path, required) tuples.
        :rtype: list
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def get_data_exports(self, aircraft):
        '''
        Returns details of data exports configuration for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: data exports info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def get_airport(self, code):
        '''
        Returns details of an airport matching the provided code.

        :param code: airport id, ICAO code or IATA code.
        :type code: int or str
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def get_nearest_airport(self, latitude, longitude):
        '''
        Returns the nearest airport to the provided latitude and longitude.

        :param latitude: latitude in decimal degrees.
        :type latitude: float
        :param longitude: longitude in decimal degrees.
        :type longitude: float
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        raise NotImplementedError


class HTTPHandler(MethodInterface, api.HTTPHandler):

    def __init__(self):
        assert settings.API_HTTP_BASE_URL, 'Setting missing for HTTP API Handler.'

    def get_aircraft(self, aircraft):
        '''
        Returns details of an aircraft matching the provided tail number.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: aircraft info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        url = '%(base_url)s/api/aircraft/%(aircraft)s/' % {
            'base_url': settings.API_HTTP_BASE_URL.rstrip('/'),
            'aircraft': aircraft.strip().lower(),
        }
        return self.request(url)

    def get_analyser_profiles(self, aircraft):
        '''
        Returns details of analyser profiles enabled for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: analyser profiles in (module_path, required) tuples.
        :rtype: list
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        url = '%(base_url)s/api/aircraft/%(aircraft)s/profiles/' % {
            'base_url': settings.API_HTTP_BASE_URL.rstrip('/'),
            'aircraft': aircraft.strip().lower(),
        }
        return self.request(url)

    def get_data_exports(self, aircraft):
        '''
        Returns details of data exports configuration for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: data exports info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        url = '%(base_url)s/api/aircraft/%(aircraft)s/exports/' % {
            'base_url': settings.API_HTTP_BASE_URL.rstrip('/'),
            'aircraft': aircraft.strip().lower(),
        }
        return self.request(url)

    def get_airport(self, code):
        '''
        Returns details of an airport matching the provided code.

        :param code: airport id, ICAO code or IATA code.
        :type code: int or str
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        url = '%(base_url)s/api/airport/%(code)s/' % {
            'base_url': settings.API_HTTP_BASE_URL.rstrip('/'),
            'code': str(code).strip().lower(),
        }
        return self.request(url)

    def get_nearest_airport(self, latitude, longitude):
        '''
        Returns the nearest airports to the provided latitude and longitude.

        :param latitude: latitude in decimal degrees.
        :type latitude: float
        :param longitude: longitude in decimal degrees.
        :type longitude: float
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        :raises: TypeError -- if the provided lat/lon are none/masked.
        :raises: ValueError -- if the provided lat/lon are oustside of valid ranges
        '''
        if any(x is None or x is np.ma.masked or np.isnan(x) for x in (latitude, longitude)):
            raise TypeError('Latitude and Longitude must be numeric.')
        if not -90 <= latitude <= 90:
            raise ValueError(u'Latitude must be between -90° and 90°: %s.', latitude)
        if not -180 <= longitude <= 180:
            raise ValueError(u'Longitude must be between -180° and 180°: %s.', longitude)
        url = '%(base_url)s/api/airport/nearest/' % {
            'base_url': settings.API_HTTP_BASE_URL.rstrip('/'),
        }
        # Note: Only need three decimal places as sufficiently accurate.
        #       Also more opportunity for caching similar responses.
        #       See https://gis.stackexchange.com/a/8674 for details.
        params = {'ll': '%.3f,%.3f' % (latitude, longitude), 'all': 1}
        return self.request(url, params=params)


class FileHandler(MethodInterface, api.FileHandler):

    def __init__(self):
        assert settings.API_FILE_PATHS, 'Setting missing for File API Handler.'

    def get_aircraft(self, aircraft):
        '''
        Returns details of an aircraft matching the provided tail number.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: aircraft info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        data = self.request(settings.API_FILE_PATHS['aircraft'])
        try:
            return data[aircraft]
        except KeyError:
            raise api.NotFoundError('Aircraft not found using Local File API: %s' % aircraft)

    def get_analyser_profiles(self, aircraft):
        '''
        Returns details of analyser profiles enabled for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: analyser profiles in (module_path, required) tuples.
        :rtype: list
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        logger.warning('Analyser profiles not supported by Local File API.')
        return []

    def get_data_exports(self, aircraft):
        '''
        Returns details of data exports configuration for an aircraft.

        :param aircraft: aircraft tail number.
        :type aircraft: str
        :returns: data exports info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        data = self.request(settings.API_FILE_PATHS['exports'])
        try:
            return data[aircraft]
        except (KeyError, TypeError):
            raise api.NotFoundError('Aircraft not found using Local File API: %s' % aircraft)

    def get_airport(self, code):
        '''
        Returns details of an airport matching the provided code.

        :param code: airport id, ICAO code or IATA code.
        :type code: int or str
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        data = self.request(settings.API_FILE_PATHS['airports'])
        for airport in data:
            if code in (airport.get('id'), airport['code'].get('iata'), airport['code'].get('icao')):
                return airport
        raise api.NotFoundError('Airport not found using Local File API: %s' % code)

    def get_nearest_airport(self, latitude, longitude):
        '''
        Returns the nearest airports to the provided latitude and longitude.

        :param latitude: latitude in decimal degrees.
        :type latitude: float
        :param longitude: longitude in decimal degrees.
        :type longitude: float
        :returns: airport info dictionary
        :rtype: dict
        :raises: api.NotFoundError -- if the aircraft cannot be found.
        '''
        data = self.request(settings.API_FILE_PATHS['airports'])
        airports = []
        for airport in data:
            if 'latitude' not in airport or 'longitude' not in airport:
                continue
            args = (latitude, longitude, airport['latitude'], airport['longitude'])
            airport['distance'] = library.bearing_and_distance(*args)[1]
            airports.append(airport)
        try:
            return airports
        except:
            raise api.NotFoundError('Airport not found using Local File API: %f,%f' % (latitude, longitude))
