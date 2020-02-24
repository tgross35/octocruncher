import json, urllib.request, os
from difflib import SequenceMatcher

# This is the type of datasheet found in the json file
# Takes in a datasheet json object and
class Datasheet:
    date_created = None
    last_updated = None
    num_pages = None
    size_bytes = None
    date_created = None
    mimetype = None
    url = None
    source = None

    def __init__(self, datasheetobj):
        if datasheetobj is None: return
        if datasheetobj['metadata'] is not None:
            self.date_created = datasheetobj['metadata'].get('date_created')
            self.last_updated = datasheetobj['metadata'].get('last_updated')
            self.num_pages = datasheetobj['metadata'].get('num_pages')
            self.size_bytes = datasheetobj['metadata'].get('size_bytes')
            self.date_created = datasheetobj['metadata'].get('date_created')
        self.mimetype = datasheetobj['mimetype']
        self.url = datasheetobj['url']

        # print(datasheetobj)
        if datasheetobj['attribution']['sources'] is not None:
            self.source = datasheetobj['attribution']['sources'][0].get('name')

    def __respr__(self):
        return self.source

# This is the type of description object found in octopart json
class Description:
    value = None
    source = None

    def __init__(self, descriptionobj):
        if descriptionobj is None: return
        self.value = descriptionobj.get('value')
        self.source = descriptionobj['attribution']['sources'][0].get('name')

    def __respr__(self):
        return self.value

class Manufacturer:
    name = None
    homepage_url = None

    def __init__(self, manufacturerobj):
        if manufacturerobj is None: return
        self.name = manufacturerobj['name']
        self.homepage_url = manufacturerobj.get('homepage_url')

class PartOffer:
    in_stock_quantity = None

    def __init__(self, offerobj):
        if offerobj is None: return
        self.in_stock_quantity = offerobj.get('in_stock_quantity')

class SpecValue:
    display_value = None
    value = None
    max_value = None
    min_value = None

    def __init__(self, specobj):
        if specobj is None: return
        self.display_value = specobj.get('display_value')
        if specobj.get('value'): self.value = specobj.get('value')[0]
        self.max_value = specobj.get('max_value')
        self.min_value = specobj.get('min_value')

    def __respr__(self):
        return '{}: {}'.format(self.name, self.value)

class OctoCruncher:
    def __init__(self,
                 mpn=None,
                 file_source=None,
                 json_source=None
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

    def getMPN(self):
        return self.octoresp['results'][0]['items'][self.itemnumber]['mpn']


    def getManufacturer(self):
        return Manufacturer(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['manufacturer'])

    # Returns a Datasheet object
    def getDatasheet(self, datasheetnumber=0):
        return Datasheet(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['datasheets'][datasheetnumber])

    # Returns a datasheet object
    def getDescription(self, descriptionnumber=0):
        return Description(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'][descriptionnumber])

    # This gets a parameter from the 'specs' dict of a response item
    def getSpec(self, specname):
        return SpecValue(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['specs'].get(specname))


    # This does about the same thing but doesn't need an exact match
    def getSpecFuzzy(self, specname):
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

        return self.getSpec(max_key)

    # Get the number of datasheets
    def getNumDatasheets(self):
        return len(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['datasheets'])

    # Get the number of descriptions
    def getNumDescriptions(self):
        return len(self.octoresp['results'][0]['items'][self.itemnumber]\
            ['descriptions'])

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
