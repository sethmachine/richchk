"""Maps a section name to a ChkSection object, e.g. "TRG " to ChkTrg.

"""

from . import chkunk, chkstr, chkunix, chkunis

_SECTIONS = [chkstr.ChkStr, chkunix.ChkUnix, chkunis.ChkUnis]
_NAME2SECTION = {sect.name: sect for sect in _SECTIONS}


def name2section(name: str):
    """Returns the class constructor for the CHK section.  Defaults to ChkUnk if no match found.
    
    :param name: 
    :return: 
    """
    sect = _NAME2SECTION.get(name)
    if not sect:
        return chkunk.ChkUnk
    else:
        return sect


if __name__ == '__main__':
    pass
