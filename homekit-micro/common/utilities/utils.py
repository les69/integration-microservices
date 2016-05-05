
def to_dict(device):
    dict = {}
    attributes = filter(lambda attribute: not str(attribute).__contains__('_'), dir(device))
    for attr in attributes:
        try:
            dict[attr] = device.__getattribute__(attr)
        except Exception:
            pass

    return dict
