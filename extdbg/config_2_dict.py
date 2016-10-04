import ConfigParser


def config_2_dict(filename):
    """Reads config file, and returns dictionary of it's sections."""
    p = ConfigParser.ConfigParser()
    res = p.read(filename)
    if res[0] != filename:
        raise IOError('Config %r was not read' % filename)

    d = dict(p._sections)
    for k in d:
        d[k] = dict(p._defaults, **d[k])
        d[k].pop('__name__', None)
    return d
