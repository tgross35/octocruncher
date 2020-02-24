# classes.py
# Data types found in an Octopart response

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

        if datasheetobj['attribution']['sources'] is not None:
            self.source = datasheetobj['attribution']['sources'][0].get('name')

    def __str__(self):
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

    def __repr__(self):
        return '{}'.format(self.name)

class PartOffer:
    eligible_region = None
    factory_lead_days = None
    factory_order_multiple = None
    in_stock_quantity = None
    is_authorized = None
    is_realtime = None
    last_updated = None
    moq = None
    multipack_quantity = None
    octopart_rfq_url = None
    on_order_eta = None
    on_order_quantity = None
    order_multiple = None
    packaging = None
    product_url = None
    seller = None
    sku = None
    seller = None

    def __init__(self, offerobj):
        if offerobj is None: return
        self.in_stock_quantity = offerobj.get('in_stock_quantity')
        self.eligible_region = offerobj.get('eligible_region')
        self.factory_lead_days = offerobj.get('factory_lead_days')
        self.factory_order_multiple = offerobj.get('factory_order_multiple')
        self.in_stock_quantity = offerobj.get('in_stock_quantity')
        self.is_authorized = offerobj.get('is_authorized')
        self.is_realtime = offerobj.get('is_realtime')
        self.last_updated = offerobj.get('last_updated')
        self.moq = offerobj.get('moq')
        self.multipack_quantity = offerobj.get('multipack_quantity')
        self.octopart_rfq_url = offerobj.get('octopart_rfq_url')
        self.on_order_eta = offerobj.get('on_order_eta')
        self.on_order_quantity = offerobj.get('on_order_quantity')
        self.order_multiple = offerobj.get('order_multiple')
        self.packaging = offerobj.get('packaging')
        self.product_url = offerobj.get('product_url')
        self.sku = offerobj.get('sku')
        self.seller = Seller(offerobj.get('seller'))

    def __repr__(self):
        return '{}: {}'.format(self.seller.name, self.sku)

class Seller:
    display_flag = None
    has_ecommerce = None
    homepage_url = None
    id = None
    name = None
    uid = None

    def __init__(self, sellerobj):
        if sellerobj is None: return
        self.display_flag = sellerobj.get('display_flag')
        self.has_ecommerce = sellerobj.get('has_ecommerce')
        self.homepage_url = sellerobj.get('homepage_url')
        self.id = sellerobj.get('id')
        self.name = sellerobj.get('name')
        self.uid = sellerobj.get('uid')

    def __repr__(self):
        return '{}: {}'.format(self.name, self.id)

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

    def __repr__(self):
        return '{}: {}'.format(self.display_value, self.value)
