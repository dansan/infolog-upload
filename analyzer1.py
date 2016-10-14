# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016: see commit history at
# https://github.com/dansan/infolog-upload/commits/master/analyzer1.py
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from infolog_upload.analyzer import InfologAnalyzer


class InfologAnalyzer1(InfologAnalyzer):
    """
    Stuff from https://github.com/spring/spring-infolog goes here
    """

    def __init__(self, logger, infolog, replay):
        super(InfologAnalyzer1, self).__init__(logger, infolog, replay)
        self.name = "Infolog Analyzer the First"

    def analyse(self):
        """
        Analyse the text in self.infolog["infolog_text"] and return data to be stored in DB.

        :return: dict: {"severity": None or one of Infolog.SEVERITY_CHOICES: "Low", "Normal", "High"
                        "ext_link": None or str (URL to issue tracker),
                        "subscribe": list of existing usernames from Users [str, str, ...],
                        "tags": list of tag names  [str, str, ...]}
        """
        return {"severity": None, "ext_link": None, "subscribe": [], "tags": []}
