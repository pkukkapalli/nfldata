import us
import postal.parser

CITY_NAME_SUBSTITUTIONS = {
    'foxborough': 'foxboro',
    'philadephia': 'philadelphia'
}


def parse_address(address):
    address = {
        key: value for value, key in postal.parser.parse_address(address)
    }
    city = address['city'] if 'city' in address else None
    city = CITY_NAME_SUBSTITUTIONS[
        city] if city in CITY_NAME_SUBSTITUTIONS else city
    state = normalize_state(address['state']) if 'state' in address else None
    return _Address(state=state, city=city)


def normalize_state(state):
    if state.lower() == 'jersey':
        state = 'new jersey'
    elif state.lower() == 'd.c.':
        state = 'dc'
    try:
        return us.states.lookup(state).abbr
    except:
        raise ValueError(f'Invalid state: {state}')


class _Address:

    def __init__(self, city, state):
        self.city = city
        self.state = state
