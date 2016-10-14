# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import base64
import re
import hashlib

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

from jsonrpc import jsonrpc_method

from srs.common import all_page_infos
from srs.models import Replay
from infolog_upload.models import Infolog, InfologTag
from forms import InfologUploadForm, NewTagForm
from analyze_thread import AnalyzeThread

logger = logging.getLogger("srs.infolog")
_il = logging.FileHandler(settings.LOG_PATH + '/jsonrpc_debug.log')
_il.setLevel(logging.DEBUG)
_il.setFormatter(logging.Formatter(fmt=settings.DEBUG_FORMAT, datefmt=settings.LOG_DATETIME_FORMAT))
logger.addHandler(_il)


@login_required
def index(request):
    c = all_page_infos(request)
    user = request.user
    if user.userprofile.is_developer:
        c["infologs"] = Infolog.objects.all()
        c["subscribed_infologs"] = Infolog.objects.filter(subscribed=user)
        return render_to_response('infolog_upload/index.html', c, context_instance=RequestContext(request))
    elif user.infolog_uploader.exists():
        c["infologs"] = Infolog.objects.filter(uploader=user)
        c["subscribed_infologs"] = Infolog.objects.filter(subscribed=user)
        return render_to_response('infolog_upload/index.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse(not_allowed, args=["_none_"]))


@jsonrpc_method('upload_json(String, String, String, Boolean, dict) -> dict', validate=True, authenticated=True)
def upload_json(request, infolog, client, freetext, has_support_ticket, extensions):
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

    return _save_infolog(user, infolog_dec.strip(), client, freetext_dec.strip(), has_support_ticket,
                         extensions=extensions)


def _save_infolog(user, infolog, client, free_text, has_support_ticket, extensions, severity="Normal"):
    # logger.debug("user: %s, infolog: %s, client: %s, free_text: %s, has_support_ticket: %s, extensions: %s, "
    #              "severity: %s", user, infolog, client, free_text, has_support_ticket, extensions, severity)

    logger.debug("user: %s, client: %s, has_support_ticket: %s, extensions: %s, severity: %s", user, client,
                 has_support_ticket, extensions, severity)
    logger.debug("free_text: '%s'", free_text)
    logger.debug("infolog(%s, len: %d): '%s' ... '%s'", type(infolog), len(infolog), infolog[:30], infolog[-30:])

    sha256 = hashlib.sha256(base64.b64encode(infolog.encode("utf-8"))).hexdigest()
    # not using get_or_create() to save comparison of infolog_text
    try:
        il = Infolog.objects.get(infolog_text_sha256=sha256)
    except ObjectDoesNotExist:
        il = Infolog.objects.create(infolog_text_sha256=sha256, infolog_text=infolog, uploader=user, client=client)

    il.free_text = free_text
    il.uploader = user
    il.client = client
    il.has_support_ticket = has_support_ticket

    try:
        il_infos = _basic_parse(infolog)
        il.replay = il_infos["replay"]
        il.game = il_infos["game"]
        # TODO: severity?
        # TODO: extensions?
    except ObjectDoesNotExist:
        pass
    finally:
        il.save()

    # TODO: trigger an email to inform game dev if it is marked as supportticket (-> #2)

    AnalyzeThread(il).start()

    return {"status": 0, "id": int(il.id), "msg": "Success.", "url": il.get_absolute_url()}


@login_required
@never_cache
def infolog_view(request, infologid):
    c = all_page_infos(request)
    infolog = get_object_or_404(Infolog, id=infologid)
    c["infolog"] = infolog
    c["comment_obj"] = infolog
    c["replay"] = infolog.replay
    user = request.user

    if request.method == 'POST':
        # dev wants to subscribe to infolog changes
        infolog.subscribed.add(user)

    if user == infolog.uploader or user.userprofile.is_developer:
        return render_to_response('infolog_upload/infolog.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse(not_allowed, args=[infolog.uploader]))


def not_allowed(request, uploader):
    c = all_page_infos(request)
    c["uploader"] = uploader
    return render_to_response('infolog_upload/not_allowed.html', c, context_instance=RequestContext(request))


def _basic_parse(infolog):
    out = {"replay": None, "game": None}

    m = re.search(r"\[.*\] GameID: (\w+)", infolog)
    if m:
        gameid = m.group(1)
        out["replay"] = Replay.objects.get(gameID=gameid)
        out["game"] = out["replay"].game
    return out


@login_required
def upload_html(request):
    c = all_page_infos(request)
    if request.method == 'POST':
        form = InfologUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data:
                infolog_file = request.FILES['infolog_file']
                if infolog_file.content_type == "text/plain":
                    free_text = form.cleaned_data['free_text']
                    has_support_ticket = form.cleaned_data['has_support_ticket']
                    severity = form.cleaned_data['severity']
                    il_text = infolog_file.read()
                    infolog_file.close()
                    il_text2 = unicode(il_text, errors='replace')
                    out = _save_infolog(request.user, il_text2.strip(), "manual upload", free_text, has_support_ticket,
                                        {}, severity)
                    return HttpResponseRedirect(out["url"])
                else:
                    c["status"] = 4
                    c["msg"] = "Not a infolog.txt file."
    else:
        form = InfologUploadForm()
    c['form'] = form
    return render_to_response('infolog_upload/upload.html', c, context_instance=RequestContext(request))


@login_required
@never_cache
def modal_manage_tags(request, infologid):
    user = request.user
    infolog = get_object_or_404(Infolog, id=infologid)
    if not (user == infolog.uploader or user.userprofile.is_developer):
        return HttpResponseRedirect(reverse(not_allowed, args=[infolog.uploader]))

    c = all_page_infos(request)
    if request.method == 'POST':
        form = NewTagForm(request.POST)
        if form.is_valid():
            if form.cleaned_data:
                name = form.cleaned_data.get("name")
                if name:
                    ilt, _ = InfologTag.objects.get_or_create(name=name.strip())
                    infolog.tags.add(ilt)
                    return HttpResponseRedirect(reverse(infolog_view, args=[infolog.id]))
        else:
            if form.instance and isinstance(form.instance, InfologTag):
                # error was 'Infolog tag with this Name already exists.'. Ignored.
                try:
                    ilt = InfologTag.objects.get(name=form.instance.name)
                    infolog.tags.add(ilt)
                    return HttpResponseRedirect(reverse(infolog_view, args=[infolog.id]))
                except:
                    pass
    else:
        form = NewTagForm()
    c["infolog"] = infolog
    c["all_tags"] = InfologTag.objects.exclude(id__in=infolog.tags.values_list("id", flat=True))
    c["newtagform"] = form
    return render_to_response('infolog_upload/modal_manage_tags.html', c, context_instance=RequestContext(request))


@login_required
@never_cache
def modal_manage_tags_rm(request, infologid, tagid):
    user = request.user
    infolog = get_object_or_404(Infolog, id=infologid)

    if not (user == infolog.uploader or user.userprofile.is_developer):
        return HttpResponseRedirect(reverse(not_allowed, args=[infolog.uploader]))

    infolog.tags.remove(InfologTag.objects.get(id=tagid))
    return HttpResponseRedirect(reverse(infolog_view, args=[infolog.id]))


@login_required
@never_cache
def modal_manage_tags_add(request, infologid, tagid):
    user = request.user
    infolog = get_object_or_404(Infolog, id=infologid)

    if not (user == infolog.uploader or user.userprofile.is_developer):
        return HttpResponseRedirect(reverse(not_allowed, args=[infolog.uploader]))

    infolog.tags.add(InfologTag.objects.get(id=tagid))
    return HttpResponseRedirect(reverse(infolog_view, args=[infolog.id]))
