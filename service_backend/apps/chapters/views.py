from functools import wraps
from rest_framework.response import Response

from service_backend.apps.chapters.models import Chapter
from rest_framework.views import APIView

from service_backend.apps.subjects.models import Subject
from service_backend.apps.utils.constants import ChapterErrorCode, SubjectErrorCode, UserRole
from service_backend.apps.utils.views import response_json, check_role
from service_backend.apps.chapters.serializers import ChapterSerializer


# Create your views here.
def find_chapter():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                chapter = Chapter.objects.get(id=args[1].data['chapter_id'])
            except Exception:
                return Response(response_json(
                    success=False,
                    code=ChapterErrorCode.CHAPTER_DOES_NOT_EXIST,
                    message="can't find chapter!"
                ), status=404)
            return func(*args, **kwargs, chapter=chapter)

        return wrapper

    return decorated


class ChapterList(APIView):
    def post(self, request):
        try:
            subject = Subject.objects.get(id=request.data['subject_id'])
        except Exception:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message="can't find subject!"
            ), status=404)
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
        except Exception:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message="can't find subject!"
            ), status=404)
        name = request.data['name']
        content = request.data['content']
        chapter = Chapter(name=name, content=content, subject=subject)
        try:
            chapter.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_SAVE_FAILED,
                message="can't save chapter!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="create chapter success!"
        ))


class ChapterUpdate(APIView):
    @find_chapter()
    def post(self, request, chapter):
        chapter.name = request.data['name']
        chapter.content = request.data['content']
        try:
            chapter.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_SAVE_FAILED,
                message="can't update chapter!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="update chapter success!"
        ))


class ChapterDelete(APIView):
    @find_chapter()
    def delete(self, request, chapter):
        try:
            chapter.delete()
        except Exception:
            return Response(response_json(
                success=False,
                code=ChapterErrorCode.CHAPTER_DELETE_FAILED,
                message="can't delete chapter!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="delete chapter success!"
        ))
