from service_backend.apps.utils.constants import GlobalCode


def response_json(success, code=None, message=None, data=None):
    success = not not success
    code = (GlobalCode.SUCCESS if success else GlobalCode.SYSTEM_FAILED) if code is None else code
    message = ("Success!" if success else "Failed!") if message is None else message

    return {
        'success': success,
        'code': code,
        'message': message,
        'data': data
    }
