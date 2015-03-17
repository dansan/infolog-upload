# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from srs.common import all_page_infos

logger = logging.getLogger(__package__)


@login_required
def index(request):
    c = all_page_infos(request)
    return render_to_response('infolog-upload/index.html', c, context_instance=RequestContext(request))
