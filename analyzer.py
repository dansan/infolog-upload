# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class InfologAnalyzer(object):
    """
    Inherit from this class and implement analyse()
    """
    def __init__(self, logger, infolog, replay):
        self.name = "Give me a name"
        self.logger = logger
        self.infolog = infolog  # see infolog_upload/models.py -> Infolog.to_dict()
        self.replay = replay    # see srs/models.py -> Replay.to_dict(), may be {} if not (yet) uploaded

    def analyse(self):
        """
        Analyse the text in self.infolog["infolog_text"] and return data to be stored in DB.

        :return: dict: {"severity": None or one of Infolog.SEVERITY_CHOICES: "Low", "Normal", "High"
                        "ext_link": None or str (URL to issue tracker),
                        "subscribe": list of existing usernames from Users [str, str, ...],
                        "tags": list of tag names  [str, str, ...]}
        """
        raise NotImplementedError("Implement me")
