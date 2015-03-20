# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User

from srs.models import Game, Replay


class Infolog(models.Model):
    infolog_text = models.TextField()
    free_text = models.TextField(blank=True)
    replay = models.ForeignKey(Replay, blank=True, null=True)
    uploader = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    client = models.CharField(max_length=256)
    has_support_ticket = models.BooleanField()
    severity = models.CharField(max_length=32, blank=True)
    game = models.ForeignKey(Game, blank=True, null=True)

    def __unicode__(self):
        return u"(%04d, %s) %s | %s" % (self.id, self.upload_date.strftime("%Y-%m-%d"), self.replay.title,
                                        self.infolog_text[:30])

    @models.permalink
    def get_absolute_url(self):
        return "infolog_upload.views.infolog_view", [self.id]
