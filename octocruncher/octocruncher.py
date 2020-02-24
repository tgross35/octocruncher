import json, urllib.request, os
from difflib import SequenceMatcher
from .classes import Datasheet, Description, Manufacturer, PartOffer, SpecValue

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
    def setItemNumber(self, itemnumber=0):
        self.itemnumber = itemnumber

    def getNumItems(self):
        return len(self.octoresp['results'][0].get('items'))

    def getMPN(self):
        return self.octoresp['results'][0]['items'][self.itemnumber].get('mpn')

    def getManufacturer(self):
        return Manufacturer(self.octoresp['results'][0]['items'][self.itemnumber]\
            .get('manufacturer'))

    def getNumOffers(self):
        return len(self.octoresp['results'][0]['items'][self.itemnumber]['offers'])

    def getOffer(self, sellernumber=0):
        return PartOffer(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['offers'][sellernumber])

    # Get the number of datasheets
    def getNumDatasheets(self):
        return len(self.octoresp['results'][0]['items'][self.itemnumber]\
        .get('datasheets'))

    # Returns a Datasheet object
    def getDatasheet(self, datasheetnumber=0):
        print('test')
        return Datasheet(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['datasheets'][datasheetnumber])

    # Get the number of descriptions
    def getNumDescriptions(self):
        return len(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'])

    # Returns a datasheet object
    def getDescription(self, descriptionnumber=0):
        return Description(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'][descriptionnumber])

    # This gets a parameter from the 'specs' dict of a response item
    def getSpec(self, specname):
        return SpecValue(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['specs'].get(specname))


    # This does about the same thing as GetSpe cbut doesn't need an exact match
    def getSpecFuzzy(self, specname):
        return self.getSpecFuzzyCloseness(specname)[0]


    # This does about the same thing as getSpec but doesn't need an exact match
    # Returns a tuple with the spec and its closeness rating
    def getSpecFuzzyCloseness(self, specname):
        # a dict that holds {spec_name, closeness_rating} e.g. {'resistance_tolerance', 9}
        howclose = {}

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

    # This does a json dump that can later be loaded by
    def getJSON(self):
        return self.octoresp
    #Helper functions

    # Actually ask octopart for a response, or use the config file
    def __queryOctopart(self):
        if self.file_source is not None:
            with open(self.file_source) as f:
                self.octoresp = json.load(f)

            self.item = self.octoresp['results'][0]['items'][0]

            return

        if self.using_json: return

        print(self.mpn)
        # Build url for query
        # todo: quote URL
        url = 'http://octopart.com/api/v3/parts/match?'
        url += '&queries=[{"mpn":"' + self.mpn + '"}]'
        url += '&apikey=' + self.api_key
        url += '&include[]=datasheets&include[]=descriptions&include[]=specs'

        print(url)
        #
        # # Try to get the return from the cache
        # data = cache.get(cachekey)
        #
        # # If it doesn't exist (i.e. timed out or never run), run the query and cache it
        # if data is None:
        #     print("Querying API for {}".format(mpn))
        self.octoresp = json.loads(urllib.request.urlopen(url).read())
        self.item = self.octoresp['results'][0]['items'][0]

        return
