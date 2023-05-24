class GlobalCode:
    SUCCESS = 0
    SYSTEM_FAILED = 1


class UserRole:
    ALL_USERS = [0, 1, 2]
    ADMIN_ONLY = [2, ]
    STUDENT = 0
    TUTOR = 1
    ADMIN = 2


DEFAULT_AVATAR = "https://shieask.com/pic/default_avatar.png"


# 问题状态，0：未认领(默认)，1：已认领，2：未认领复审 3: 已认领复审 4: 有效提问 5: 无效提问
class IssueStatus:
    NOT_ADOPT = 0
    ADOPTING = 1
    NOT_REVIEW = 2
    REVIEWING = 3
    VALID_ISSUE = 4
    INVALID_ISSUE = 5


class NotificationCategory:
    GLOBAL = 0
    Issue = 1


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
    USER_LOAD_FAILED = 208


class SubjectErrorCode:
    SUBJECT_SAVE_FAILED = 301
    SUBJECT_DOES_NOT_EXIST = 302
    SUBJECT_DELETE_FAILED = 303
    SUBJECT_LIST_UPDATE_FAILED = 304


class ChapterErrorCode:
    CHAPTER_SAVE_FAILED = 401
    CHAPTER_DOES_NOT_EXIST = 402
    CHAPTER_DELETE_FAILED = 403


class TagErrorCode:
    TAG_SAVE_FAILED = 501
    TAG_DOES_NOT_EXIST = 502
    TAG_DELETE_FAILED = 503


class IssueErrorCode:
    ISSUE_NOT_FOUND = 601
    ISSUE_DELETE_FAILED = 602
    ISSUE_SAVED_FAILED = 603
    REVIEW_ISSUE_QUERY_FAILED = 604
    ADOPT_ISSUE_QUERY_FAILED = 605
    FOLLOW_ISSUE_QUERY_FAILED = 606
    ASK_ISSUE_QUERY_FAILED = 607
    ISSUE_ACTION_REJECT = 608
    ISSUE_RELATE_FAILED = 609


class IssueLikeErrorCode:
    ISSUE_LIKE_SAVED_FAILED = 701
    ISSUE_LIKE_DELETE_FAILED = 702


class IssueFollowErrorCode:
    ISSUE_FOLLOW_SAVED_FAILED = 701
    ISSUE_FOLLOW_DELETE_FAILED = 702


class IssueTagErrorCode:
    ISSUE_TAG_SAVED_FAILED = 801
    ISSUE_TAG_DELETE_FAILED = 802


class IssueReviewerErrorCode:
    REVIEWER_ISSUE_SAVED_FAILED = 901


class OtherErrorCode:
    UNEXPECTED_JSON_FORMAT = 1001


class ImageErrorCode:
    IMAGE_LOAD_FAILED = 1101
    WRONG_IMAGE_FORMAT = 1102
    UNEXPECTED_IMAGE_NAME = 1103
    IMAGE_SAVE_FAILED = 1104
    INVALID_IMAGE_FORMAT = 1105
    IMAGE_TOO_BIG = 1106


class CommentErrorCode:
    COMMENT_NOT_FOUND = 1201
    COMMENT_DELETE_FAILED = 1202
    COMMENT_SAVED_FAILED = 1203


class DraftErrorCode:
    DRAFT_SAVE_FAILED = 1301
    DRAFT_LOAD_FAILED = 1302


class NotificationErrorCode:
    NOTIFICATION_SAVE_FAILED = 1401
    NOTIFICATION_LOAD_FAILED = 1402
    NOTIFICATION_DELETE_FAILED = 1403
    NOTIFICATION_RECEIVER_SAVE_FAILED = 1404
    NOTIFICATION_RECEIVER_LOAD_FAILED = 1405


class MailErrorCode:
    MAIL_CONFIRM_FAILED = 1501
    MAIL_FORMAT_WRONG = 1502
