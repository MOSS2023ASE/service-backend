from functools import wraps
from rest_framework.response import Response

from service_backend.apps.tags.models import Tag
from rest_framework.views import APIView

from service_backend.apps.utils.constants import TagErrorCode
from service_backend.apps.utils.views import response_json
from service_backend.apps.tags.serializers import TagSerializer


# Create your views here.
def _find_tag():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                tag = Tag.objects.get(id=args[1].data['tag_id'])
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=TagErrorCode.TAG_DOES_NOT_EXIST,
                    message="can't find tag!"
                ))
            return func(*args, **kwargs, tag=tag)

        return wrapper

    return decorated


class TagList(APIView):
    def get(self, request):
        tag = Tag.objects.all()
        tag_serializer = TagSerializer(tag, many=True)
        data = {'tag_list': tag_serializer.data}
        return Response(response_json(
            success=True,
            data=data
        ))


class TagCreate(APIView):
    def post(self, request):
        content = request.data['content']
        tag = Tag(content=content)
        try:
            tag.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=TagErrorCode.TAG_SAVE_FAILED,
                message="can't save tag!"
            ))

        return Response(response_json(
            success=True,
            message="create tag success!"
        ))


class TagUpdate(APIView):
    @_find_tag()
    def post(self, request, tag):
        tag.content = request.data['content']
        try:
            tag.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=TagErrorCode.TAG_SAVE_FAILED,
                message="can't update tag!"
            ))

        return Response(response_json(
            success=True,
            message="update tag success!"
        ))


class TagDelete(APIView):
    @_find_tag()
    def post(self, request, tag):
        try:
            tag.delete()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=TagErrorCode.TAG_DELETE_FAILED,
                message="can't delete tag!"
            ))
        return Response(response_json(
            success=True,
            message="delete tag success!"
        ))
