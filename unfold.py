import json
from copy import deepcopy


def get_json():
    files = ['simcir-library.js', 'devices.js']
    result = {}
    for file in files:
        with open(file) as f:
            counter = 0
            js = ''
            for line in f.readlines():
                for char in line:
                    if char == '{':
                        counter += 1
                    if counter > 0:
                        js += char
                    if char == '}':
                        counter -= 1
                    if js != '' and counter == 0:
                        j = json.loads(js)
                        js = ''
                        result[j['name']] = j
    return result


def get_data():
    with open('code.json') as f:
        return json.load(f)


def get_next_id(m):
    m[0] += 1
    return str(m[0])


def remove_in(con_remove_in, new_type):
    for con in con_remove_in:
        dev_id = con['to'].split('.')[0]
        for dev_con in new_type['connectors']:
            back_id = dev_con['from'].split('.')[0]
            if back_id == dev_id:
                remove_in([dev_con], new_type)
        for x in new_type['devices']:
            if x['id'] == dev_id:
                rem_obj = x
                break
        try:
            new_type['devices'].remove(rem_obj)
        except UnboundLocalError:
            pass
        try:
            new_type['connectors'].remove(con)
        except UnboundLocalError:
            pass





m = [0]
blue_prints = get_json()
blue_prints_names = blue_prints.keys()
data = get_data()
for device in data['devices']:
    if device['type'] in blue_prints_names:
        # New Type Modification
        new_type = deepcopy(blue_prints[device['type']])
        ins = []
        outs = []
        ids = {}
        con_remove_in = []
        con_remove_out = []
        for new_device in new_type['devices']:
            # Unique Id Generation
            old_id = new_device['id']
            new_id = get_next_id(m)
            ids[old_id] = new_id
            new_device['id'] = new_id
            if new_device['type'] == 'In':
                ins.append(new_id)
            if new_device['type'] == 'Out':
                outs.append(new_id)

        for new_con in new_type['connectors']:
            # Modify connection for new ids
            fro = new_con['from']
            con_id, index = fro.split('.')
            fro = ids[con_id] + '.' + index
            new_con['from'] = fro
            if ids[con_id] in ins:
                con_remove_in.append(new_con)

            to = new_con['to']
            con_id, index = to.split('.')
            to = ids[con_id] + '.' + index
            new_con['to'] = to
            if ids[con_id] in outs:
                con_remove_out.append(new_con)
        # Remove everything what isn't necessary
        remove_in(con_remove_in, new_type)
        if con_remove_out:
            print('Warnung', con_remove_out)

        # Normalize
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        for new_device in new_type['devices']:
            # Collect information
            if new_device['x'] > max_x:
                max_x = new_device['x']

            if new_device['y'] > max_y:
                max_y = new_device['y']

            if new_device['x'] < min_x:
                min_x = new_device['x']

            if new_device['y'] < min_y:
                min_y = new_device['y']
        for new_device in new_type['devices']:
            new_device['x'] += device['x'] - min_x
            new_device['y'] += device['y'] - min_y

        dev_width = max_x - min_x
        dev_height = max_y - min_y
        # Parent Modifications
        data['devices'].remove(device)

        for parent_device in data['devices']:
            if parent_device['x'] >= device['x'] and parent_device['y'] >= device['y'] + 16 * max(len(ins), len(outs)):
                parent_device['y'] += dev_height

            if parent_device['y'] >= device['y'] and parent_device['x'] >= device['x'] + 64:
                parent_device['x'] += dev_width

        data['devices'] += new_type['devices']
        data['connectors'] = new_type['connectors']
        break
print(json.dumps(data))
