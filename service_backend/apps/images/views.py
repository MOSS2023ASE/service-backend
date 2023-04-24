from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.settings import MEDIA_ROOT, STATIC_URL
from service_backend.apps.users.models import User
from service_backend.apps.utils.views import check_role, response_json
from service_backend.apps.utils.constants import ImageErrorCode, UserRole

import os
import uuid
import imghdr
from datetime import datetime

PIC_URL_BASE = "http://shieask.com/pic/"
# PIC_URL_BASE = 'http://localhost:8000'


# Create your views here.
class UploadAvatar(APIView):

    def post(self, request, action_user=None):
        pass


class UploadImage(APIView):

    @check_role(UserRole.ALL_USERS)
    def post(self, request, action_user: User = None):
        try:
            image = request.data['file']
            image_type = imghdr.what(image)
            # print(type(image))
        except Exception as _e:
            # raise _e
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_LOAD_FAILED,
                message="image load failed!"
            ))
        if image.size > (5 << 20):
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_TOO_BIG,
                message="size of uploaded image can't exceed 5MB!"
            ))
        if image_type is None:
            return Response(response_json(
                success=False,
                code=ImageErrorCode.INVALID_IMAGE_FORMAT,
                message="not an image-format file!"
            ))

        image_root = os.path.join(MEDIA_ROOT)
        image_name = action_user.student_id + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + str(uuid.uuid4()) + '.' + image_type
        image_path = os.path.join(image_root, image_name)
        print(image_root)
        print(image_name)
        # get file
        img_suffix = image.name.split('.')[-1]
        if image_type != ('jpeg' if img_suffix == 'jpg' else img_suffix):
            return Response(response_json(
                success=False,
                code=ImageErrorCode.UNEXPECTED_IMAGE_NAME,
                message='wrong image suffix!'
            ))
        # store file
        try:
            print(image_root)
            if not os.path.exists(image_root):
                os.mkdir(image_root)
            with open(image_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                f.close()
            print(PIC_URL_BASE + STATIC_URL)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=ImageErrorCode.IMAGE_SAVE_FAILED,
                message='image save failed!'
            ))
        return Response(response_json(
            success=True,
            message='upload image successfully!',
            data={
                'url': PIC_URL_BASE + image_name
            }
        ))
