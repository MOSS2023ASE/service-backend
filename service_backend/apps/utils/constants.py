class GlobalCode:
    SUCCESS = 0
    SYSTEM_FAILED = 1


class UserRole:
    STUDENT = 0
    TUTOR = 1
    ADMIN = 2


class YearErrorCode:
    YEAR_SAVE_FAILED = 101
    YEAR_DOES_NOT_EXIST = 102
    YEAR_DELETE_FAILED = 103


class UserErrorCode:
    USER_NOT_FOUND = 201
    INCORRECT_PASSWORD = 202
    EXPIRED_JWT = 203
    INVALID_JWT = 204
    USER_SAVE_FAILED = 205
    USER_FROZEN = 206
    PERMISSION_DENIED = 207


class IssueErrorCode:
    ISSUE_NOT_FOUND = 301
    ISSUE_DELETE_FAILED = 302
    ISSUE_SAVED_FAILED = 303


class OtherErrorCode:
    UNEXPECTED_JSON_FORMAT = 901


class SubjectErrorCode:
    SUBJECT_SAVE_FAILED = 301
    SUBJECT_DOES_NOT_EXIST = 302
    SUBJECT_DELETE_FAILED = 303


class ChapterErrorCode:
    CHAPTER_SAVE_FAILED = 401
    CHAPTER_DOES_NOT_EXIST = 402
    CHAPTER_DELETE_FAILED = 403


class TagErrorCode:
    TAG_SAVE_FAILED = 501
    TAG_DOES_NOT_EXIST = 502
    TAG_DELETE_FAILED = 503
