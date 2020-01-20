# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016-2020 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django_comments.models import Comment


class InfologTag(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class Infolog(models.Model):
    SEVERITY_CHOICES = (("Low", "Low: No hurry."),
                        ("Normal", "Normal (default): A developer should look at this."),
                        ("High", "High: Game is unplayable!"))

    infolog_text = models.TextField()
    free_text = models.TextField(blank=True)
    replay = models.ForeignKey("srs.Replay", blank=True, null=True, on_delete=CASCADE)
    uploader = models.ForeignKey(User, related_name="infolog_uploader", on_delete=CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    client = models.CharField(max_length=256)
    has_support_ticket = models.BooleanField(default=False)
    severity = models.CharField(max_length=32, choices=SEVERITY_CHOICES, default="Normal", blank=True)
    game = models.ForeignKey("srs.Game", blank=True, null=True, on_delete=CASCADE)
    ext_link = models.URLField(blank=True)
    subscribed = models.ManyToManyField(User, blank=True, related_name="subscriber")
    tags = models.ManyToManyField(InfologTag, blank=True)
    infolog_text_sha256 = models.CharField(max_length=64, unique=True)
    replay_gameID = models.CharField(max_length=32, blank=True, db_index=True)

    def __unicode__(self):
        return u"Infolog({}, {}, {})".format(self.pk, self.upload_date.strftime("%Y-%m-%d"), self.replay)

    def get_absolute_url(self):
        return reverse("infolog_upload/show", args=[self.id])

    @property
    def comments_count(self):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get(model="infolog")
        return Comment.objects.filter(content_type=ct, object_pk=self.pk).count()

    def is_subscribed(self, user):
        return self.subscribed.filter(id=user.id).exists()

    def to_dict(self):
        return {"id": self.id,
                "infolog_text": self.infolog_text,
                "free_text": self.free_text,
                "replay": self.replay.title if self.replay else "FIXME: no replay",
                "replay_id": self.replay.id if self.replay else 0,  # "FIXME: no replay"
                "uploader": self.uploader.username,
                "upload_date": self.upload_date,
                "client": self.client,
                "has_support_ticket": self.has_support_ticket,
                "severity": self.severity,
                "game": self.game.name if self.game else "FIXME: no game",
                "game_id": self.game.id if self.game else 0,  # "FIXME: no game"
                "game_devs": ",".join(self.game.developer.all().values_list("username", flat=True)) if self.game and
                self.game.developer.exists() else "",
                "ext_link": self.ext_link,
                "subscribed": self.subscribed,
                "tags": ",".join(self.tags.all().values_list("name", flat=True)) if self.tags and self.tags.exists() else "",
                "infolog_text_sha256": self.infolog_text_sha256}
