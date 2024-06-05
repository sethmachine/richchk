"""Enumerate all the known public function names of StormLib."""

from enum import Enum


class StormLibOperation(Enum):
    GET_LAST_ERROR = ("GetLastError",)
    S_FILE_SET_LOCALE = ("SFileSetLocale",)
    S_FILE_OPEN_ARCHIVE = ("SFileOpenArchive",)
    S_FILE_CREATE_ARCHIVE = ("SFileCreateArchive",)
    S_FILE_CREATE_ARCHIVE2 = ("SFileCreateArchive2",)
    S_FILE_SET_DOWNLOAD_CALLBACK = ("SFileSetDownloadCallback",)
    S_FILE_FLUSH_ARCHIVE = ("SFileFlushArchive",)
    S_FILE_CLOSE_ARCHIVE = ("SFileCloseArchive",)
    S_FILE_ADD_LIST_FILE = ("SFileAddListFile",)
    S_FILE_SET_COMPACT_CALLBACK = ("SFileSetCompactCallback",)
    S_FILE_COMPACT_ARCHIVE = ("SFileCompactArchive",)
    S_FILE_GET_MAX_FILE_COUNT = ("SFileGetMaxFileCount",)
    S_FILE_SET_MAX_FILE_COUNT = ("SFileSetMaxFileCount",)
    S_FILE_GET_ATTRIBUTES = ("SFileGetAttributes",)
    S_FILE_SET_ATTRIBUTES = ("SFileSetAttributes",)
    S_FILE_UPDATE_FILE_ATTRIBUTES = ("SFileUpdateFileAttributes",)
    S_FILE_OPEN_PATCH_ARCHIVE = ("SFileOpenPatchArchive",)
    S_FILE_IS_PATCHED_ARCHIVE = ("SFileIsPatchedArchive",)
    S_FILE_HAS_FILE = ("SFileHasFile",)
    S_FILE_OPEN_FILE_EX = ("SFileOpenFileEx",)
    S_FILE_GET_FILE_SIZE = ("SFileGetFileSize",)
    S_FILE_SET_FILE_POINTER = ("SFileSetFilePointer",)
    S_FILE_READ_FILE = ("SFileReadFile",)
    S_FILE_CLOSE_FILE = ("SFileCloseFile",)
    S_FILE_GET_FILE_INFO = ("SFileGetFileInfo",)
    S_FILE_GET_FILE_NAME = ("SFileGetFileName",)
    S_FILE_FREE_FILE_INFO = ("SFileFreeFileInfo",)
    S_FILE_EXTRACT_FILE = ("SFileExtractFile",)
    S_FILE_GET_FILE_CHECKSUMS = ("SFileGetFileChecksums",)
    S_FILE_VERIFY_FILE = ("SFileVerifyFile",)
    S_FILE_VERIFY_RAW_DATA = ("SFileVerifyRawData",)
    S_FILE_SIGN_ARCHIVE = ("SFileSignArchive",)
    S_FILE_VERIFY_ARCHIVE = ("SFileVerifyArchive",)
    S_FILE_FIND_FIRST_FILE = ("SFileFindFirstFile",)
    S_FILE_FIND_NEXT_FILE = ("SFileFindNextFile",)
    S_FILE_FIND_CLOSE = ("SFileFindClose",)
    S_LIST_FILE_FIND_FIRST_FILE = ("SListFileFindFirstFile",)
    S_LIST_FILE_FIND_NEXT_FILE = ("SListFileFindNextFile",)
    S_LIST_FILE_FIND_CLOSE = ("SListFileFindClose",)
    S_FILE_ENUM_LOCALES = ("SFileEnumLocales",)
    S_FILE_CREATE_FILE = ("SFileCreateFile",)
    S_FILE_WRITE_FILE = ("SFileWriteFile",)
    S_FILE_FINISH_FILE = ("SFileFinishFile",)
    S_FILE_ADD_FILE_EX = ("SFileAddFileEx",)
    S_FILE_ADD_FILE = ("SFileAddFile",)
    S_FILE_ADD_WAVE = ("SFileAddWave",)
    S_FILE_REMOVE_FILE = ("SFileRemoveFile",)
    S_FILE_RENAME_FILE = ("SFileRenameFile",)
    S_FILE_SET_FILE_LOCALE = ("SFileSetFileLocale",)
    S_FILE_SET_DATA_COMPRESSION = ("SFileSetDataCompression",)
    S_FILE_SET_ADD_FILE_CALLBACK = ("SFileSetAddFileCallback",)
    S_COMP_IMPLODE = ("SCompImplode",)
    S_COMP_EXPLODE = ("SCompExplode",)
    S_COMP_COMPRESS = ("SCompCompress",)
    S_COMP_DECOMPRESS = ("SCompDecompress",)
    S_COMP_DECOMPRESS2 = ("SCompDecompress2",)

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value
