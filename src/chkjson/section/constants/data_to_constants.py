"""Turns a data file into a Python file with constants.

"""

import ast
import json
import re


def line_to_constant(line, separator='='):
    parts = line.split(separator)
    value = int(parts[0].strip())
    name = parts[1].strip()
    name = re.sub(r'[ \(\)/\?\+]', '_', name)
    name = re.sub(r'[\'\-]', '', name)
    name = name.strip('_')
    name = name.replace('__', '_')
    val = '{}: "{}"'.format(value, parts[1].strip())
    const = '{} = {}'.format(name.upper(), value)
    return const, val


def datafile_to_constants(infile, separator='='):
    constants = []
    vals = []
    with open(infile, 'r') as f:
        for line in f:
            const, val = line_to_constant(line, separator)
            constants.append(const)
            vals.append(val)
    return constants, vals


def vals_to_dict(vals, name):
    raw_dict = '{{{}}}'.format(', '.join(vals))
    real_dict = ast.literal_eval(raw_dict)
    pretty_dict = json.dumps(real_dict, indent=1)
    pretty_dict = re.sub(r'"([0-9]+)"', r'\1', pretty_dict)
    return '{} = {}'.format(name, pretty_dict)


def constants_to_python(constants, vals, name, outfile):
    with open(outfile, 'w') as f:
        f.write('\n'.join(constants))
        f.write('\n')
        f.write(vals_to_dict(vals, name))
        f.write('\n')
    return outfile


if __name__ == '__main__':
    # c, v = datafile_to_constants('../data/unit_ids.txt')
    # constants_to_python(c, v, 'ID_TO_UNIT', 'unit_ids.py')
    c, v = datafile_to_constants('../data/weapon_ids.txt')
    constants_to_python(c, v, 'ID_TO_WEAPON', 'weapon_ids.py')
