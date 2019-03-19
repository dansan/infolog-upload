# This file is part of the "spring relay site / srs" program. It is published
# under the GPLv3.
#
# Copyright (C) 2016 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.forms import ModelForm

from infolog_upload.models import Infolog, InfologTag

import logging

logger = logging.getLogger(__name__)


class InfologUploadForm(forms.Form):
    infolog_file = forms.FileField(label="infolog.txt")
    free_text = forms.CharField(label="Description", widget=forms.Textarea)
    has_support_ticket = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "checkbox"}), required=False,
                                            initial="False", label="This is a support ticket:")
    severity = forms.ChoiceField(required=False, choices=Infolog.SEVERITY_CHOICES,
                                 widget=forms.Select(attrs={"style": "color: #000000"}))


class NewTagForm(ModelForm):
    class Meta:
        model = InfologTag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control input-sm", "placeholder": "New Tag"}),
        }
