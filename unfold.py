import json
from copy import deepcopy
import operator


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
        ok = True
        for dev in new_type['devices']:
            if dev['id'] == dev_id:
                if dev['type'] not in ['Toggle', 'DC', 'PushOn', 'PushOff']:
                    ok = False
                break
        if not ok:
            continue

        for dev_con in new_type['connectors']:
            back_id = dev_con['from'].split('.')[0]
            if back_id == dev_id:
                remove_in([dev_con], new_type)

        for x in new_type['devices']:
            if x['id'] == dev_id and x['type'] in ['Toggle', 'DC', 'PushOn', 'PushOff']:
                new_type['devices'].remove(x)
                break
        try:
            new_type['connectors'].remove(con)
        except ValueError:
            pass

def remove_out(con_remove_ou, new_type):
    for con in con_remove_in:
        dev_id = con['to'].split('.')[0]
        ok = True
        for dev in new_type['devices']:
            if dev['id'] == dev_id:
                # if dev['type'] not in ['Toggle', 'DC', 'PushOn', 'PushOff']:
                ok = False
                # print(dev['type'])
                break
        if not ok:
            continue

        for dev_con in new_type['connectors']:
            back_id = dev_con['from'].split('.')[0]
            if back_id == dev_id:
                remove_out([dev_con], new_type)

        # for x in new_type['devices']:
        #     if x['id'] == dev_id and x['type'] in ['Toggle', 'DC', 'PushOn', 'PushOff']:
        #         new_type['devices'].remove(x)
        #         break
        # try:
        #     new_type['connectors'].remove(con)
        # except ValueError:
        #     pass


def cord_sort(dict):
    x, y = dict['x'], dict['y']
    x *= 1000000000
    return x + y


def get_value(name, history):
    if name in list(history.keys()):
        return history[name]
    if name not in blue_prints_names:
        if name == 'Toggle' or name == 'DC':
            return 0
        return 1
    blue_print = blue_prints[name]
    total = 0
    for dev in blue_print['devices']:
        total += get_value(dev['type'], history)
    history[name] = total
    return total


history = {}
m = [0]
blue_prints = get_json()
blue_prints_names = list(blue_prints.keys())
data = get_data()
t = 0
for dev in data['devices']:
    t += get_value(dev['type'], history)

factor = 1 / 10
sorted_history = sorted(history.items(), key=operator.itemgetter(1))
sorted_history.append((data, -1))
for blue_print in blue_prints.values():
    try:
        value = len(blue_print['devices'])
    except KeyError:
        value = 1
    blue_print['width'] = int(blue_print['width'] * factor * value)
    blue_print['height'] = int(blue_print['height'] * factor * value)
    for dev in blue_print['devices']:
        dev['x'] = int(dev['x'] * factor * value)
        dev['y'] = int(dev['y'] * factor * value)

value = len(data['devices'])
data['width'] = int(data['width'] * factor * value / 2)
data['height'] = int(data['height'] * factor * value / 2)
for dev in data['devices']:
    dev['x'] = int(dev['x'] * factor * value / 2)
    dev['y'] = int(dev['y'] * factor * value / 2)

for name, k in sorted_history:
    if k >= 0:
        data = deepcopy(blue_prints[name])
    else:
        data = name
    finished = False
    while not finished:
        for device in data['devices']:
            finished = True
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
                        ins.append({'id': new_id, 'x': new_device['x'], 'y':  new_device['y']})
                    if new_device['type'] == 'Out':
                        outs.append({'id': new_id, 'x': new_device['x'], 'y':  new_device['y']})
                ins = sorted(ins, key=cord_sort)
                outs = sorted(outs, key=cord_sort)
                for new_con in new_type['connectors']:
                    # Modify connection for new ids
                    fro = new_con['from']
                    con_id, index = fro.split('.')
                    fro = ids[con_id] + '.' + index
                    new_con['from'] = fro
                    if ids[con_id] in [x['id'] for x in ins]:
                        con_remove_in.append(new_con)

                    to = new_con['to']
                    con_id, index = to.split('.')
                    to = ids[con_id] + '.' + index
                    new_con['to'] = to
                    if ids[con_id] in [x['id'] for x in outs]:
                        con_remove_out.append(new_con)
                # Remove everything what isn't necessary
                remove_in(con_remove_in, new_type)
                remove_out(con_remove_out, new_type)
                if con_remove_out:
                    print('Warnung', con_remove_out)
                    pass
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
                dev_small_height = 16 * max(len(ins), len(outs))
                # Parent Modifications
                data['devices'].remove(device)
                for parent_device in data['devices']:
                    #  device['y'] + dev_height + 65 >=
                    if parent_device['x'] >= device['x'] and device['y'] + dev_height >= parent_device['y'] >= device['y'] + dev_small_height-1:
                        parent_device['y'] += dev_height
                    # device['x'] + dev_width + 65 >=
                    if parent_device['y'] >= device['y'] and device['x'] + dev_width >= parent_device['x'] >= device['x'] + 63:
                        parent_device['x'] += dev_width

                dev_id = device['id']
                for con in data['connectors']:
                    fro = con['from']
                    con_id, index = fro.split('.')
                    if con_id == dev_id:
                        num_index = int(index[2:])
                        fro = ins[num_index]['id'] + '.in0'
                        con['from'] = fro

                    to = con['to']
                    con_id, index = to.split('.')
                    if con_id == dev_id:
                        num_index = int(index[3:])
                        to = outs[num_index]['id'] + '.out0'
                        con['to'] = to

                for devi in new_type['devices']:
                    if devi['type'] == 'In':
                        devi['type'] = 'Joint'
                    if devi['type'] == 'Out':
                        devi['type'] = 'Joint'

                data['devices'] += new_type['devices']
                data['connectors'] += new_type['connectors']
                finished = False
                break

    cords_x = [0]
    cords_y = [0]
    for dev in data['devices']:
        # if dev['type'] != 'Joint' and dev['type'] != 'In' and dev['type'] != 'Out':
        cords_x.append(dev['x'])
        cords_y.append(dev['y'])
    cords_x.sort()
    cords_y.sort()
    sm_x = []
    for cord_last, cords_new in zip(cords_x[:-1], cords_x[1:]):
        if cords_new - cord_last > 42:
            sm_x.append((cords_new-1, cords_new-cord_last-42))
    sm_y = []
    for cord_last, cords_new in zip(cords_y[:-1], cords_y[1:]):
        if cords_new - cord_last > 42:
            sm_y.append((cords_new-1, cords_new-cord_last-42))

    for dev in data['devices']:
        total = 0
        for m_x in sm_x:
            if dev['x'] >= m_x[0]:
                total += m_x[1]
        dev['x'] -= total
        total = 0
        for m_y in sm_y:
            if dev['y'] >= m_y[0]:
                total += m_y[1]
        dev['y'] -= total

    max_x, max_y = float('-inf'), float('-inf')
    for device in data['devices']:
        if device['x'] > max_x:
            max_x = device['x']

        if device['y'] > max_y:
            max_y = device['y']
    data['width'] = max_x + 150
    data['height'] = max_y + 64

    if k >= 0:
        blue_prints[name] = deepcopy(data)
        if name == '':
            print(json.dumps(data))
    else:
        pass

total_dev = len([x for x in data['devices'] if x['type'] != 'Joint'])
total_joints = len([x for x in data['devices'] if x['type'] == 'Joint'])
print(total_joints)

print(total_dev, len(data['connectors']) - total_joints)

print(json.dumps(data))
