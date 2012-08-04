from .models import User


class UserMiddleware(object):
    def process_request(self, request):
        twitter_id = request.session.get('twitter_id')

        if twitter_id:
            try:
                request.twitter_user = User.objects.get(twitter_id=twitter_id)
                return
            except User.DoesNotExist:
                pass

        request.twitter_user = None
