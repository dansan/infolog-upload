# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
import datetime

from django.contrib.auth.models import User
from django.conf import settings

from infolog_upload.models import Infolog, InfologTag
from analyzer1 import InfologAnalyzer1

logger = logging.getLogger(__package__)
_il = logging.FileHandler(settings.LOG_PATH+'/analyse.log')
_il.setLevel(logging.DEBUG)
_il.setFormatter(logging.Formatter(fmt=settings.DEBUG_FORMAT, datefmt=settings.LOG_DATETIME_FORMAT))
logger.addHandler(_il)

class AnalyzeThread(threading.Thread):
    def __init__(self, infolog):
        self.infolog = infolog
        il_dict = self.infolog.to_dict()
        replay_dict = self.infolog.replay.to_dict() if self.infolog.replay else {}
        ila1 = InfologAnalyzer1(logger, il_dict, replay_dict)
        # more analyzers can be added here
        self.analyzers = [ila1, ]
        super(AnalyzeThread, self).__init__()

    def run(self):
        self.thread = threading.current_thread()
        self.thread.start_time = datetime.datetime.now()
        logger.info("Running in thread '%s'.", self.thread.name)
        for analyzer in self.analyzers:
            logger.info("Starting analyzer '%s'.", analyzer.name)
            try:
                result = analyzer.analyse()
            except:
                logger.exception("Error running analyzer '%s'.", analyzer.name)
                continue
            logger.debug("Analyzer '%s' returned data: '%s'.", analyzer.name, result)
            try:
                if result.get("severity") in [k for k, _ in Infolog.SEVERITY_CHOICES]:
                    self.infolog.severity = result["severity"]
                if result.get("ext_link"):
                    self.infolog.ext_link = result["ext_link"]
                for username in result.get("subscribe", []):
                    try:
                        user = User.objects.get(username=username)
                        self.infolog.subscribed.add(user)
                    except:
                        logger.error("No user found with username='%s'.", username)
                for tag in result.get("tags", []):
                    ilt, _ = InfologTag.objects.get_or_create(name=tag)
                    self.infolog.tags.add(ilt)
                self.infolog.save()
            except:
                logger.exception("Error in result of analyzer '%s'.", analyzer.name)
        logger.info("All analyzers ran, thread finished after %d seconds.", (datetime.datetime.now() -
                                                                               self.thread.start_time).seconds)
