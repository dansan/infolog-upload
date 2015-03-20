# -*- coding: utf-8 -*-

# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django import test

from jsonrpc.proxy import ServiceProxy

from test_logins import *


class TestInfologUpload(test.TestCase):
    # fixtures = []

    def test_authenticate_with_InfologUpload_success(self):
        sp = ServiceProxy(test_url)
        out = sp.upload(lobby_username, lobby_password, "infolog text blah blah", "client name", "some free text",
                        False, {})
        self.assertIsNone(out["error"])
        self.assertEqual(out["result"]["status"], 0)
