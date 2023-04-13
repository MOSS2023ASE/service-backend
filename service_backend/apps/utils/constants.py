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
    PRIVILEGE_SAVE_FAILED = 206
    USER_FROZEN = 207
    PERMISSION_DENIED = 208



