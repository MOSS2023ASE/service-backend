from functools import wraps
from rest_framework.response import Response

from service_backend.apps.chapters.models import Chapter
from rest_framework.views import APIView

from service_backend.apps.subjects.models import Subject
from service_backend.apps.utils.constants import ChapterErrorCode, SubjectErrorCode
from service_backend.apps.utils.views import response_json
from service_backend.apps.chapters.serializers import ChapterSerializer


# Create your views here.
def _find_chapter():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                chapter = Chapter.objects.get(id=args[1].data['chapter_id'])
            except Exception as e:
                return Response(response_json(
                    success=False,
                    code=ChapterErrorCode.CHAPTER_DOES_NOT_EXIST,
                    message="can't find chapter!"
                ))
            return func(*args, **kwargs, chapter=chapter)

        return wrapper

    return decorated


class ChapterList(APIView):
    def post(self, request):
        try:
            subject = Subject.objects.get(id=request.data['subject_id'])
        except Exception as e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message="can't find subject!"
            ))
        chapter_serializer = ChapterSerializer(subject.chapters, many=True)
        data = {'chapter_list': chapter_serializer.data}
        return Response(response_json(
            success=True,
            data=data
        ))


class ChapterCreate(APIView):
    def post(self, request):
        try:
            subject = Subject.objects.get(id=request.data['subject_id'])
        except Exception as e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message="can't find subject!"
            ))
        name = request.data['name']
        content = request.data['content']
        chapter = Chapter(name=name, content=content, subject=subject)
        try:
            chapter.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_SAVE_FAILED,
                message="can't save chapter!"
            ))

        return Response(response_json(
            success=True,
            message="create chapter success!"
        ))


class ChapterUpdate(APIView):
    @_find_chapter()
    def post(self, request, chapter):
        chapter.name = request.data['name']
        chapter.content = request.data['content']
        try:
            chapter.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_SAVE_FAILED,
                message="can't update chapter!"
            ))

        return Response(response_json(
            success=True,
            message="update chapter success!"
        ))


class ChapterDelete(APIView):
    @_find_chapter()
    def delete(self, request, chapter):
        try:
            chapter.delete()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_DELETE_FAILED,
                message="can't delete chapter!"
            ))
        return Response(response_json(
            success=True,
            message="delete chapter success!"
        ))
