from collections import defaultdict


def gen_fields(rec, fields):
    for field in fields:
        yield field, str(getattr(rec, field))


#TODO: make Table class for outputting data into it
#TODO: format header
def make_table(row, shape, attrs):
    fmt_data = "|"
    fmt_line= "+"
    for attr in attrs:
        fmt_data += "{"+f"{attr.lower()}:"+"^"+f"{shape[attr.lower()]+round(shape[attr.lower()]*0.5)}"+"}"+"|"
        fmt_line += "="*(shape[attr.lower()]+round(shape[attr.lower()]*0.5))+"+"
    print(fmt_line)
    print(fmt_data.format(**row))


def table_shape(data_obj, attrs):
    """Returns length of longest fields from `Record`."""
    rv = defaultdict(int)
    for rec in data_obj:
        for key, val in gen_fields(rec, attrs):
            if rv[key] < len(val):
                rv[key]  = len(val)
    return rv
