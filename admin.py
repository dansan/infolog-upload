# This file is part of the "infolog-upload" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016-2020 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin

from .models import Infolog, InfologTag


class InfologAdmin(admin.ModelAdmin):
    list_display = (
        "replay",
        "id",
        "severity",
        "game",
        "uploader",
        "upload_date",
        "has_support_ticket",
    )
    search_fields = [
        "id",
        "infolog_text",
        "free_text",
        "replay__title",
        "uploader__username",
        "ext_link",
    ]
    list_filter = (
        "severity",
        "game",
        "has_support_ticket",
        "client",
        "upload_date",
        "replay__unixTime",
    )


admin.site.register(Infolog, InfologAdmin)
admin.site.register(InfologTag)
