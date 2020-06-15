# classes.py
# Data types found in an Octopart response

# This is the type of datasheet found in the json file
# Takes in a datasheet json object and
class Datasheet:
    date_created = ''
    last_updated = ''
    num_pages = ''
    size_bytes = ''
    date_created = ''
    mimetype = ''
    url = ''
    source = ''

    def __init__(self, datasheetobj=None):
        if datasheetobj is None: return
        if datasheetobj['metadata'] is not None:
            self.date_created = datasheetobj['metadata'].get('date_created', '')
            self.last_updated = datasheetobj['metadata'].get('last_updated', '')
            self.num_pages = datasheetobj['metadata'].get('num_pages', '')
            self.size_bytes = datasheetobj['metadata'].get('size_bytes', '')
            self.date_created = datasheetobj['metadata'].get('date_created', '')
        self.mimetype = datasheetobj['mimetype']
        self.url = datasheetobj['url']

        if datasheetobj['attribution']['sources'] is not None:
            self.source = datasheetobj['attribution']['sources'][0].get('name', '')

    def __repr__(self):
        return self.source

# This is the type of description object found in octopart json
class Description:
    value = ''
    source = ''

    def __init__(self, descriptionobj=None):
        if descriptionobj is None: return
        self.value = descriptionobj.get('value', '')
        self.source = descriptionobj['attribution']['sources'][0].get('name', '')

    def __repr__(self):
        return self.value

class Manufacturer:
    name = ''
    homepage_url = ''

    def __init__(self, manufacturerobj):
        if manufacturerobj is None: return
        self.name = manufacturerobj.get('name', '')
        self.homepage_url = manufacturerobj.get('homepage_url', '')

    def __repr__(self):
        return self.name


class Seller:
    name = ''
    display_flag = ''
    has_ecommerce = ''
    homepage_url = ''
    id = ''
    uid = ''

    def __init__(self, sellerobj=None):
        if sellerobj is None: return
        self.display_flag = sellerobj.get('display_flag', '')
        self.has_ecommerce = sellerobj.get('has_ecommerce', '')
        self.homepage_url = sellerobj.get('homepage_url', '')
        self.id = sellerobj.get('id', '')
        self.name = sellerobj.get('name', '')
        self.uid = sellerobj.get('uid', '')

    def __repr__(self):
        return '{}: {}'.format(self.name, self.id)

class PartOffer:
    eligible_region = ''
    factory_lead_days = ''
    factory_order_multiple = ''
    in_stock_quantity = ''
    is_authorized = ''
    is_realtime = ''
    last_updated = ''
    moq = ''
    multipack_quantity = ''
    octopart_rfq_url = ''
    on_order_eta = ''
    on_order_quantity = ''
    order_multiple = ''
    packaging = ''
    product_url = ''
    seller = ''
    sku = ''
    seller = Seller()

    def __init__(self, offerobj):
        if offerobj is None: return
        self.in_stock_quantity = offerobj.get('in_stock_quantity', '')
        self.eligible_region = offerobj.get('eligible_region', '')
        self.factory_lead_days = offerobj.get('factory_lead_days', '')
        self.factory_order_multiple = offerobj.get('factory_order_multiple', '')
        self.in_stock_quantity = offerobj.get('in_stock_quantity', '')
        self.is_authorized = offerobj.get('is_authorized', '')
        self.is_realtime = offerobj.get('is_realtime', '')
        self.last_updated = offerobj.get('last_updated', '')
        self.moq = offerobj.get('moq', '')
        self.multipack_quantity = offerobj.get('multipack_quantity', '')
        self.octopart_rfq_url = offerobj.get('octopart_rfq_url', '')
        self.on_order_eta = offerobj.get('on_order_eta', '')
        self.on_order_quantity = offerobj.get('on_order_quantity', '')
        self.order_multiple = offerobj.get('order_multiple', '')
        self.packaging = offerobj.get('packaging', '')
        self.product_url = offerobj.get('product_url', '')
        self.sku = offerobj.get('sku', '')
        self.seller = Seller(offerobj.get('seller', None))

    def __repr__(self):
        return '{}: {}'.format(self.seller.name, self.sku)


class SpecValue:
    name = ''
    display_value = ''
    value = ''
    max_value = ''
    min_value = ''

    def __init__(self, specobj, name=''):
        if specobj is None: return
        self.name = name
        self.display_value = specobj.get('display_value')
        if specobj.get('value'): self.value = specobj.get('value')[0]
        self.max_value = specobj.get('max_value')
        self.min_value = specobj.get('min_value')

    def __repr__(self):
        return '{}: {}'.format(self.name, self.display_value)

    def __str__(self):
        return '{}: {}'.format(self.name, self.display_value)