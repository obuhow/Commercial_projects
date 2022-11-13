from .parser import SweetSpeakParser
from .models import ScheduledPosts


def shedule_post_module():
    # initialize parser
    sweetspeak = SweetSpeakParser()
    # run parser main function
    sweetspeak.make_new_posts()
    # print result
    db = ScheduledPosts.objects.all()
    i = 1
    for feed in db:
        print('Запланированный пост №', i)
        print(feed.sending_datetime, feed.post)
        i += 1


shedule_post_module()
