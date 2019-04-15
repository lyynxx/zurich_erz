"""Support for RESTful API sensors."""
import logging
import json
import datetime

import voluptuous as vol
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_FORCE_UPDATE, CONF_HEADERS, CONF_NAME,
    CONF_RESOURCE, CONF_TIMEOUT,
    HTTP_DIGEST_AUTHENTICATION)
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Zurich ERZ Sensor'
DEFAULT_FORCE_UPDATE = False
DEFAULT_TIMEOUT = 10

CALENDARS = ['cardboard', 'cargotram', 'etram', 'metal', 'organic', 'paper', 'special', 'textile', 'waste']
CONF_CAL_CARDBOARD = 'cardboard'
CONF_CAL_CARGOTRAM = 'cargotram'
CONF_CAL_ETRAM = 'etram'
CONF_CAL_METAL = 'metal'
CONF_CAL_ORGANIC = 'organic'
CONF_CAL_PAPER = 'paper'
CONF_CAL_SPECIAL = 'special'
CONF_CAL_TEXTILE = 'textile'
CONF_CAL_WASTE = 'waste'

CONF_ZIP = 'zip'
CONF_TOUR = 'tour'

RESOURCE_CARDBOARD = 'http://openerz.metaodi.ch/api/calendar/cardboard.json'
RESOURCE_CARGOTRAM = 'http://openerz.metaodi.ch/api/calendar/cargotram.json'
RESOURCE_ETRAM = 'http://openerz.metaodi.ch/api/calendar/etram.json'
RESOURCE_METAL = 'http://openerz.metaodi.ch/api/calendar/metal.json'
RESOURCE_ORGANIC = 'http://openerz.metaodi.ch/api/calendar/organic.json'
RESOURCE_PAPER = 'http://openerz.metaodi.ch/api/calendar/paper.json'
RESOURCE_SPECIAL = 'http://openerz.metaodi.ch/api/calendar/special.json'
RESOURCE_TEXTILE = 'http://openerz.metaodi.ch/api/calendar/textile.json'
RESOURCE_WASTE = 'http://openerz.metaodi.ch/api/calendar/waste.json'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ZIP): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_FORCE_UPDATE, default=DEFAULT_FORCE_UPDATE): cv.boolean,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_CAL_CARDBOARD, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_CARGOTRAM, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_ETRAM, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_METAL, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_ORGANIC, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_PAPER, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_SPECIAL, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_TEXTILE, default='false'): cv.boolean,
    vol.Optional(CONF_CAL_WASTE, default='false'): cv.boolean,
    vol.Optional(CONF_TOUR): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the RESTful sensor."""
    name = config.get(CONF_NAME)
    resource = config.get(CONF_RESOURCE)
    method = 'get'
    verify_ssl = True
    force_update = config.get(CONF_FORCE_UPDATE)
    timeout = config.get(CONF_TIMEOUT)

    zip = config.get(CONF_ZIP)
    tour = config.get(CONF_TOUR)
	
    cardboard = config.get(CONF_CAL_CARDBOARD)
    cargotram = config.get(CONF_CAL_CARGOTRAM)
    etram = config.get(CONF_CAL_ETRAM)
    metal = config.get(CONF_CAL_METAL)
    organic = config.get(CONF_CAL_ORGANIC)
    paper = config.get(CONF_CAL_PAPER)
    special = config.get(CONF_CAL_SPECIAL)
    textile = config.get(CONF_CAL_TEXTILE)
    waste = config.get(CONF_CAL_WASTE)

    rests = []
	
    if cardboard: 
        rest_cardboard = RestData('cardboard', RESOURCE_CARDBOARD, timeout, zip, tour)
        rest_cardboard.update()
        
        if rest_cardboard.data is None:
            raise PlatformNotReady
   
        rests.append(rest_cardboard)

    if cargotram:
        rest_cargotram = RestData('cargotram', RESOURCE_CARGOTRAM, timeout, zip, tour)
        rest_cargotram.update()

        if rest_cargotram.data is None:
            raise PlatformNotReady
   
        rests.append(rest_cargotram)

    if etram:
        rest_etram = RestData('etram', RESOURCE_ETRAM, timeout, zip, tour)
        rest_etram.update()

        if rest_etram is None:
            raise PlatformNotReady

        rests.append(rest_etram)

    if metal:
        rest_metal = RestData('metal', RESOURCE_METAL, timeout, zip, tour)
        rest_metal.update()

        if rest_metal.data is None:
            raise PlatformNotReady

        rests.append(rest_metal)

    if organic:	
        rest_organic = RestData('organic', RESOURCE_ORGANIC, timeout, zip, tour)
        rest_organic.update()

        if rest_organic.data is None:
            raise PlatformNotReady

        rests.append(rest_organic)

    if paper:
        rest_paper = RestData('paper', RESOURCE_PAPER, timeout, zip, tour)
        rest_paper.update()

        if rest_paper.data is None:
            raise PlatformNotReady

        rests.append(rest_paper)
		
    if special:
        rest_special = RestData('special', RESOURCE_SPECIAL, timeout, zip, tour)
        rest_special.update()

        if rest_special.data is None:
            raise PlatformNotReady

        rests.append(rest_special)

    if textile:
        rest_textile = RestData('textile', RESOURCE_TEXTILE, timeout, zip, tour)
        rest_textile.update()
    
        if rest_textile.data is None:
            raise PlatformNotReady

        rests.append(rest_textile)

    if waste:
        rest_waste = RestData('waste', RESOURCE_WASTE, timeout, zip, tour)
        rest_waste.update()

        if rest_waste.data is None:
            raise PlatformNotReady

        rests.append(rest_waste)
		
		
    # Must update the sensor now (including fetching the rest resource) to
    # ensure it's updating its state.
    add_entities([RestSensor(
        hass, rests, name,
        force_update
    )], True)
		



class RestSensor(Entity):
    """Implementation of a REST sensor."""

    def __init__(self, hass, rests, name, force_update):
        """Initialize the REST sensor."""
        self._hass = hass
        self._rests = rests
        self._name = name
        self._state = None
        self._attributes = {}
        self._force_update = force_update

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
		
    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return None

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return None

    @property
    def available(self):
        """Return if the sensor data are available."""
        return True
        """return self.rest.data is not None"""

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def force_update(self):
        """Force update."""
        return self._force_update

    def update(self):
        """Get the latest data from REST API and update the state."""
        self._state = '1'
        i = 0
        for rest in self._rests:
            i += 1

            self._attributes[rest.name] = 'undef'

            rest.update()

            value = rest.data

            json_dict = json.loads(value)	

            if 'error' in json_dict:
                self._attributes[rest.name] = 'undef'
            elif 'result' in json_dict:
                if len(json_dict["result"]) > 0:
                    self._attributes[rest.name] = json_dict["result"][0]["date"]
                else:
                    self._attributes[rest.name] = 'not specified'

            """self._attributes[rest.name] = value"""

        self._state = i

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

class RestData:
    """Class for handling the data retrieval."""

    def __init__(self, name, resource, timeout, zip, tour):
        """Initialize the data object."""
        self._name = name
        self._method = 'get'
        self._resource = resource
        self._data = None
        self._timeout = timeout
        self._tour = tour
        self._zip = zip

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    def update(self):
        """Get the latest data from REST service with provided method."""
        _LOGGER.debug("Updating from %s", self._resource)
        try:                
            url = self._resource + '?sort=date&offset=0&limit=5&zip=' + self._zip + '&start=' + datetime.datetime.now().strftime("%Y-%m-%d")
            if self._tour is not None:
                url += '&tour=' + self._tour

            request = requests.Request(
                self._method, url, data=self._data).prepare()
            
            with requests.Session() as sess:

                response = sess.send(
                    request, timeout=self._timeout)

            self.data = response.text
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s from %s failed with %s",
                          self._request, self._request.url, ex)
            self.data = None