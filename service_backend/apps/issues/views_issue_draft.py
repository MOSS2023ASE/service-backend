from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.issues.models import UserDraft, Comment
from service_backend.apps.utils.constants import UserRole, CommentErrorCode, DraftErrorCode
from service_backend.apps.utils.views import check_role, response_json


class SaveDraft(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    def post(self, request, action_user):
        chapter_id = request.data['chapter_id'] if request.data['chapter_id'] else None
        title = request.data['title'] if request.data['title'] else None
        content = request.data['content'] if request.data['content'] else None
        anonymous = request.data['anonymous'] if request.data['anonymous'] else 0

        origin_draft = UserDraft.objects.filter(user=action_user)
        if origin_draft:
            origin_draft.delete()

        draft = UserDraft(user=action_user, chapter_id=chapter_id, title=title, content=content, anonymous=anonymous)
        try:
            draft.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=DraftErrorCode.DRAFT_SAVE_FAILED,
                message="can't save draft!"
            ), status=404)
        return Response(response_json(
            success=True,
            message="save draft success!"
        ))


class LoadDraft(APIView):
    @check_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN, ])
    def post(self, request, action_user):
        user_draft = UserDraft.objects.filter(user=action_user)
        data = {
            "chapter_id": None,
            "title": None,
            "content": None,
            "anonymous": 0,
            "subject_id": None
        }

        if user_draft:
            data["chapter_id"] = user_draft.first().chapter_id
            data["title"] = user_draft.first().title
            data["content"] = user_draft.first().content
            data["anonymous"] = user_draft.first().anonymous
            if user_draft.first().chapter_id:
                data["subject_id"] = user_draft.first().chapter.subject_id

        return Response(response_json(
            success=True,
            message="load draft success!",
            data=data
        ))
