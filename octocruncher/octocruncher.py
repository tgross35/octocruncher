import json, urllib.request, os
from difflib import SequenceMatcher
from .helper_classes import Datasheet, Description, Manufacturer, PartOffer, SpecValue
from typing import Tuple, List, Any

class OctoCruncher:
    def __init__(self,
                 mpn=None,
                 json_source=None,
                 file_source=None
                 ):

        self.mpn = mpn
        self.file_source=file_source
        self.octoresp = json_source if json_source is not None else None
        self.using_json = 1 if json_source is not None else 0
        self.itemnumber = 0
        self.api_key = os.environ.get('OCTOPART_API_KEY')

        self.__queryOctopart()

    # This does nothing now but will select which responded item you want
    def setItemNumber(self, itemnumber=0) -> None:
        self.itemnumber = itemnumber

    def getNumItems(self) -> int:
        try:
            return len(self.octoresp['results'][0].get('items'))

        except IndexError:
            return 0

    def getMPN(self) -> str:
        try:
            return self.octoresp['results'][0]['items'][self.itemnumber].get('mpn')

        except IndexError:
            return ''

    def getManufacturer(self) -> Manufacturer:
        try:
            return Manufacturer(self.octoresp['results'][0]['items'][self.itemnumber]\
            .get('manufacturer'))
        except IndexError:
            return Manufacturer(None)

    def getNumOffers(self) -> int:
        try:
            return len(self.octoresp['results'][0]['items'][self.itemnumber]['offers'])

        except IndexError:
            return 0

    def getOffer(self, sellernumber=0) -> PartOffer:
        try:
            return PartOffer(listget(self.octoresp['results'][0]['items'][self.itemnumber]\
                ['offers'], sellernumber))
        except IndexError:
            return PartOffer(None)

    # Get the number of datasheets
    def getNumDatasheets(self) -> int:
        try:
            return len(self.octoresp['results'][0]['items'][self.itemnumber]\
                .get('datasheets'))
        except IndexError:
            return 0

    # Returns a Datasheet object
    def getDatasheet(self, datasheetnumber=0) -> Datasheet:
        try:
            return Datasheet(listget(self.octoresp['results'][0]['items'][self.itemnumber]\
                ['datasheets'], datasheetnumber))
        except IndexError:
            return Datasheet(None)

    # Get the number of descriptions
    def getNumDescriptions(self) -> int:
        try:
            return len(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'])
        except IndexError:
            return 0

    # Returns a datasheet object
    def getDescription(self, descriptionnumber=0) -> Description:
        try:
            return Description(listget(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'], descriptionnumber))
        except IndexError:
            return Description()

    # This gets a parameter from the 'specs' dict of a response item
    def getSpec(self, specname: str) -> SpecValue:
        try:
            return SpecValue(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['specs'].get(specname), specname)
        except IndexError:
            return SpecValue(None)

    # This does about the same thing as GetSpec but doesn't need an exact match
    def getSpecFuzzy(self, specname: str) -> SpecValue:
        try:
            return self.getSpecFuzzyCloseness(specname)[0]
        except IndexError:
            return SpecValue(None)

    # This does about the same thing as getSpec but doesn't need an exact match
    # Returns a tuple with the spec and its closeness rating
    def getSpecFuzzyCloseness(self, specname: str) -> Tuple[SpecValue, int]:
        # a dict that holds {spec_name, closeness_rating} e.g. {'resistance_tolerance', 9}
        howclose = {}

        try:
            for i in self.octoresp['results'][0]['items'][self.itemnumber]['specs']:
                if specname is None or i is None: continue
                howclose[i] = SequenceMatcher(None, specname, i).ratio()

            max = 0
            max_key = ''

            for i in howclose:
                if howclose[i] >= max:
                    max = howclose[i]
                    max_key = i

            return (self.getSpec(max_key), max)
        except IndexError:
            return(SpecValue(None), 0)

    # Returns a list of specs
    def getAllSpecs(self) -> List[SpecValue]:
        try:
            l = []
            for i in self.octoresp['results'][0]['items'][self.itemnumber]['specs']:
                l.append(SpecValue(self.octoresp['results'][0]['items'][self.itemnumber]['specs'].get(i), i))
            return l
        except IndexError:
            return []

    # Return dict with all specs
    def getSpecsJSON(self) -> Any:
        try:
            return self.octoresp['results'][0]['items'][self.itemnumber]['specs']
        except IndexError:
            return {}

    # This does a json dump that can later be loaded by
    def getJSON(self) -> Any:
        return self.octoresp
    #Helper functions

    # Actually ask octopart for a response, or use the config file
    def __queryOctopart(self) -> None:
        if self.file_source is not None:
            with open(self.file_source) as f:
                self.octoresp = json.load(f)

            self.item = self.octoresp['results'][0]['items'][0]

            return

        if self.using_json: return

        # Build url for query
        # todo: quote URL
        url = 'http://octopart.com/api/v3/parts/match?'
        url += '&queries=[{"mpn":"' + self.mpn + '"}]'
        url += '&apikey=' + self.api_key
        url += '&include[]=datasheets&include[]=descriptions&include[]=specs'

        #
        # # Try to get the return from the cache
        # data = cache.get(cachekey)
        #
        # # If it doesn't exist (i.e. timed out or never run), run the query and cache it
        # if data is None:
        #     print("Querying API for {}".format(mpn))
        self.octoresp = json.loads(urllib.request.urlopen(url).read())

        # Try to set item from response. If it doesn't exist, catch the exception
        self.item =  listget(self.octoresp['results'][0]['items'], 0)

        return

# Safew way to get from a list that may or may not exist
def listget(l, i, default=None) -> Any:
    if l is None: return None
    try:
        return l[i]
    except IndexError:
        return default
