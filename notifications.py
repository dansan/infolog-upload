# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016-2020 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from django.core.exceptions import ObjectDoesNotExist

from .models import Infolog

logger = logging.getLogger(__name__)


class Notifications(object):
    """
    Notification system.
    """

    def new_comment(self, infolog):
        logger.debug("Infolog: %s", infolog)

    @staticmethod
    def new_replay(replay):
        logger.debug("Replay: %s", replay)
        try:
            il = Infolog.objects.get(replay_gameID=replay.gameID)
            logger.info("Found replay %s to associate with Infolog %s.", replay, il)
            il.replay = replay
            il.save()
        except ObjectDoesNotExist:
            logger.info("Replay %s not associated with any Infolog.", replay)
            pass
