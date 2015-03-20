# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2015 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import base64
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from jsonrpc import jsonrpc_method

from srs.common import all_page_infos
from srs.models import Replay
from infolog_upload.models import Infolog


logger = logging.getLogger(__package__)
_il = logging.FileHandler(settings.LOG_PATH+'/jsonrpc_debug.log')
_il.setLevel(logging.DEBUG)
_il.setFormatter(logging.Formatter(fmt=settings.DEBUG_FORMAT, datefmt=settings.LOG_DATETIME_FORMAT))
logger.addHandler(_il)


@login_required
def index(request):
    c = all_page_infos(request)
    c["infologs"] = Infolog.objects.all()
    return render_to_response('infolog_upload/index.html', c, context_instance=RequestContext(request))

@jsonrpc_method('upload(String, String, String, Boolean, dict) -> dict', validate=True, authenticated=True)
def upload(request, infolog, client, freetext, has_support_ticket, extensions):
    """
    JSON-RPC upload function.
    The @jsonrpc_method decorator with authenticated=True prepends "username" and "password" arguments.

    :param username: lobby account username, implicitly added by @jsonrpc_method("...", authenticated=True)
    :type username: str
    :param password: lobby account password, implicitly added by @jsonrpc_method("...", authenticated=True)
    :type password: str
    :param request: Django request object, implicitly added by Django
    :type request: WSGIRequest
    :param infolog: content of infolog.txt
    :type infolog: str, base64 encoded
    :param client: name of the connecting client software
    :type client: str
    :param freetext: user text  (use "" is not needed)
    :type freetext: str, base64 encoded
    :param has_support_ticket: user thinks this is a support case
    :type has_support_ticket: bool
    :param extensions: additional fields w/o changing API (use {} is not needed)
    :type extensions: dict
    :return: {"status": int, "id": int, "msg": str} with status=0 if all is good, ID for this entry if
    status=0 and a user message.
    :rtype: dict
    """
    logger.info("Received upload from HTTP_USER_AGENT: '%s', REMOTE_ADDR: '%s'", request.META.get("HTTP_USER_AGENT"),
                request.META.get("REMOTE_ADDR"))
    logger.debug("infolog[:50]: '%s', freetext[:50]: '%s'", infolog[:50], freetext[:50])
    logger.debug("client: '%s', has_support_ticket: '%s', extensions: '%s'", client, has_support_ticket, extensions)

    user = request.user
    logger.debug("user: '%s'", user)

    try:
        infolog_dec = base64.b64decode(infolog)
        logger.debug("infolog_dec:[30]: %s", infolog_dec[:50])
    except TypeError, te:
        logger.error("Uploaded infolog not properly formatted: %s", te)
        return {"status": 1, "msg": "Uploaded infolog not properly formatted."}

    try:
        freetext_dec = base64.b64decode(freetext)
        logger.debug("freetext_dec:[30]: %s", freetext_dec[:50])
    except TypeError, te:
        logger.error("Uploaded freetext not properly formatted: %s", te)
        return {"status": 2, "msg": "Uploaded freetext not properly formatted."}

    il = Infolog(infolog_text=infolog_dec, free_text=freetext_dec,  uploader=user, client=client,
                 has_support_ticket=has_support_ticket)

    try:
        il_infos = _basic_parse(infolog_dec)
        il.replay = il_infos["replay"]
        il.game = il_infos["game"]
        # severity?
        il.save()
    except ObjectDoesNotExist:
        pass

    # TODO: trigger an email to inform game dev if it is marked as supportticket (-> #2)
    # TODO: analyze (-> #3)

    return {"status": 0, "id": int(il.id), "msg": "Success.", "url": il.get_absolute_url()}


def infolog_view(request, infologid):
    c = all_page_infos(request)
    c["infolog"] = get_object_or_404(Infolog, id=infologid)
    return render_to_response('infolog_upload/infolog.html', c, context_instance=RequestContext(request))


def _basic_parse(infolog):
    out = {"replay": None, "game": None}

    m = re.search(r"\[.*\] GameID: (\w+)",  infolog)
    if m:
        gameid = m.group(1)
        out["replay"] = Replay.objects.get(gameID=gameid)
        out["game"] = out["replay"].game
    return out
