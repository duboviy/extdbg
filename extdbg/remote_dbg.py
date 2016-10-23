def enable_debug(pycharm_dbg_egg_path, localhost_ip,
                 port=5678, stdoutToServer=True, stderrToServer=True):
    """
    Run this function on remote process to debug it using pycharm remote server run.
    :param pycharm_dbg_egg_path: str
        ex. "C:\Program Files (x86)\JetBrains\PyCharm 2016.1\debug-eggs\pycharm-debug.egg"
        ex. "/home/<username>/pydev/debug-eggs/pycharm-debug.egg"
    :param localhost_ip: str
        insert your localhost ip (ex."10.135.10.97") to connect using network
        or 'localhost' if you use same machine (without network connection)
    :param port: int (by default 5678)
    :param stdoutToServer: bool (by default True)
    :param stderrToServer: bool (by default True)
    """
    import pydevd   # need to have pycharm-debug.egg in sys.path to be imported
    import sys

    print('connecting to debug server...')

    sys.path.append(r'%s\pycharm-debug.egg' % pycharm_dbg_egg_path)
    pydevd.settrace(localhost_ip, port=port,
                    stdoutToServer=stdoutToServer, stderrToServer=stderrToServer)
