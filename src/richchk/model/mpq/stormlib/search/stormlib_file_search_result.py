"""Stores the data of a file found by StormLib SFileFindFirstFile or SFileFindNextFile.

struct SFILE_FIND_DATA {

char   cFileName[MAX_PATH];              // Name of the found file

char * szPlainName;                      // Plain name of the found file

DWORD  dwHashIndex;                      // Hash table index for the file

DWORD  dwBlockIndex;                     // Block table index for the file

DWORD  dwFileSize;                       // Uncompressed size of the file, in bytes

DWORD  dwFileFlags;                      // MPQ file flags

DWORD  dwCompSize;                       // Compressed file size

DWORD  dwFileTimeLo;                     // Low 32-bits of the file time (0 if not
present)

DWORD  dwFileTimeHi;                     // High 32-bits of the file time (0 if not
present)

LCID   lcLocale;                         // Locale version };
"""
from ctypes import Structure, c_char, c_char_p, c_uint16, c_uint32

# suggested max file name size, change if needed
_MAX_FILE_NAME_SIZE = 260


class StormLibFileSearchResult(Structure):
    _fields_ = [
        ("cFileName", c_char * _MAX_FILE_NAME_SIZE),
        ("szPlainName", c_char_p),
        ("dwHashIndex", c_uint32),
        ("dwBlockIndex", c_uint32),
        ("dwFileSize", c_uint32),
        ("dwFileFlags", c_uint32),
        ("dwCompSize", c_uint32),
        ("dwFileTimeLo", c_uint32),
        ("dwFileTimeHi", c_uint32),
        ("lcLocale", c_uint16),
    ]

    def __str__(self) -> str:
        return (
            f"File Name: {self.cFileName.decode('utf-8', 'ignore').rstrip(chr(0))}\n"
            f"Plain Name: {self.szPlainName.decode('utf-8', 'ignore') if self.szPlainName else None}\n"
            f"Hash Index: {self.dwHashIndex}\n"
            f"Block Index: {self.dwBlockIndex}\n"
            f"File Size: {self.dwFileSize}\n"
            f"File Flags: {self.dwFileFlags}\n"
            f"Compressed Size: {self.dwCompSize}\n"
            f"File Time Low: {self.dwFileTimeLo}\n"
            f"File Time High: {self.dwFileTimeHi}\n"
            f"Locale: {self.lcLocale}"
        )
