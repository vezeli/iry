def gen_fields(rec, fields):
    for field in fields:
        yield field, getattr(rec, field)


#TODO: make Table class for outputting data into it
#TODO: improve formatting of the line
def make_table(d, attrs):
    fmt = ""
    for attr in attrs:
        fmt += "{"+f"{attr.lower()}"+"}"
    print("=========")
    print(fmt.format(**d))


def table_shape(fields):
    #TODO: use iterator over object fields to generate size of each field
    pass
