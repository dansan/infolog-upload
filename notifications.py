# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

logger = logging.getLogger(__package__)


class Notifications(object):
    """
    Notification system.
    """
    def new_comment(self, infolog):
        logger.debug("Infolog: %s", infolog)
