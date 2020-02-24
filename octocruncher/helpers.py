# helpers.py
# All the messy functions that make octocruncher run
from difflib import SequenceMatcher

# Gives you a description from the list of them
def getDetail(specs, descriptions, type):
    type = type.lower()
    from octoconfig import description_types

    format_list = []

    if type in description_types:
        for i in range(len(description_types[type][1])):
            format_list.append(getSpecFuzzy(specs, description_types[type][1][i]))

        return description_types[type][0].format(*format_list)

    detail = ''

    # Primarily select from digikey
    for i in range(len(descriptions)):
        if 'digi' in descriptions[i]['attribution']['sources'][0]['name'].lower():
            return descriptions[i]['value']

    # If not available, go Mouser
    if detail == '':
        for i in range(len(descriptions)):
            if 'mouser' in descriptions[i]['attribution']['sources'][0]['name'].lower():
                return descriptions[i]['value']

    # If those fail, just suggest the first one
    if detail == '':
        return descriptions[0]['value']

    # If nothing else
    return ''

# Gets a nice simple value from a list of specs
def getValue(specs):
    from octoconfig import value_options

    return smash(specs, value_options)

# gets the package type
def getPackage(specs):
    return smash(specs, 'case_package')

# Mark critical if it can be replaced
def getCritical(type):
    from octoconfig import noncritical_types

    return '0' if type.lower() in noncritical_types else '1'

# This does a wild search
def getSpecFuzzy(specs, query):
    # a dict that holds {spec_name, closeness_rating} e.g. {'resistance_tolerance', 9}
    howclose = {}
    for i in specs:
        howclose[i] = SequenceMatcher(None, query, i).ratio()

    max = 0
    max_key = ''

    for i in howclose:
        if howclose[i] >= max:
            max = howclose[i]
            max_key = i

    return smash(specs, max_key)

    # return max from howclose dict



def getLibRef(specs, type):
    if type == "Resistor": return 'Resistor - Standard'
    if type == "Capacitor": return 'Capacitor - Bipolar'
    if type == "Inductor": return 'Inductor - Core'
    return ''


def getFootprintRef(package, type):
    if type == "Resistor": return 'R{}L'.format(package)
    if type == "Capacitor": return 'C{}L'.format(package)
    if type == "Inductor": return 'L{}L'.format(package)
    return ''



# This function takes a dictionary and finds an allowed value if it exists
def smash(mydict, allowable_values):
    # If only a single string, no need to iterate
    if isinstance(allowable_values, str):
        return getvalue(allowable_values.lower(), mydict)

    # Run some tests for each acceptable value
    for i in allowable_values:
        x = getvalue(i.lower(), mydict)
        if x != '': return x

    return ''

# Quick function to get display_val if avalable
def getvalue(i, mydict):
    if i in mydict:
        if 'display_value' in mydict[i]:
            return mydict[i]['display_value']
        if 'value' in mydict[i]:
            return mydict[i]['value']
        if 'min_value' in mydict[i] and 'max_value' in mydict[i]:
            return mydict[i]['min_value'] + '-' + mydict[i]['max_value']
    return ''
