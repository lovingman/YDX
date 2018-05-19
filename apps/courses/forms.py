# _*_ encoding:utf-8 _*_
from  DjangoUeditor.forms import UEditorModelForm
from operation.models import UserNote
__author__ = 'YZF'
__date__ = '2018/5/12,10:49'


class NoteUEditorModelForm(UEditorModelForm):
    class Meta:
        model = UserNote
    fields = ['note']