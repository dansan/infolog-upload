# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments import Comment

from srs.models import Game, Replay, Tag


class Infolog(models.Model):
    SEVERITY_CHOICES = (("Low", "Low: No hurry."),
                        ("Normal", "Normal (default): A developer should look at this."),
                        ("High", "High: Game is unplayable!"))

    infolog_text = models.TextField()
    free_text = models.TextField(blank=True)
    replay = models.ForeignKey(Replay, blank=True, null=True)
    uploader = models.ForeignKey(User, related_name="infolog_uploader")
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    client = models.CharField(max_length=256)
    has_support_ticket = models.BooleanField(default=False)
    severity = models.CharField(max_length=32, choices=SEVERITY_CHOICES, default="Normal", blank=True)
    game = models.ForeignKey(Game, blank=True, null=True)
    ext_link = models.URLField(blank=True)
    subscribed = models.ManyToManyField(User, related_name="subscriber")
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return u"(%04d, %s) %s | %s" % (self.id, self.upload_date.strftime("%Y-%m-%d"), self.replay,
                                        self.infolog_text[:30])

    @models.permalink
    def get_absolute_url(self):
        return "infolog_upload.views.infolog_view", [self.id]

    @property
    def comments_count(self):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get(name="infolog")
        return Comment.objects.filter(content_type=ct, object_pk=self.pk).count()

    def is_subscribed(self, user):
        return self.subscribed.filter(id=user.id).exists()
