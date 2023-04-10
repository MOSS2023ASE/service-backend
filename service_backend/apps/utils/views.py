from django.shortcuts import render


# Create your views here.
def response_json(success, code=None, message=None, data=None):
    success = not not success
    code = (0 if success else 1) if code is None else code
    message = ("Success!" if success else "Failed!") if message is None else message

    return {
        'success': success,
        'code': code,
        'message': message,
        'data': data
    }
