from django import forms
from django.core.exceptions import ValidationError


class PulsarForm(forms.Form):
    request_bytes = forms.CharField(label='Запрос (request_bytes) необязательно',
                                    required=False,
                                    initial='0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,'
                                            ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73',
                                    widget=forms.Textarea(attrs={'cols': '48', 'rows': '2'}))
    response_bytes = forms.CharField(label='Запрос (request_bytes)',
                                     initial='0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0x95, 0x13,'
                                             ' 0x61, 0x42, 0xc3, 0x5b, 0x36, 0x42, 0x48, 0xdf,'
                                             ' 0x2a, 0x41, 0x81, 0x36, 0x1e, 0x3b, 0x37, 0xd1,'
                                             ' 0x80, 0x41, 0x89, 0x3b, 0xc1, 0x44, 0x66, 0x30,'
                                             ' 0x6a, 0x3e, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,'
                                             ' 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,'
                                             ' 0xff, 0xff, 0xc7, 0x3f, 0x6a, 0x3e, 0x6c, 0x2d,'
                                             ' 0x00, 0x00, 0xba, 0x1c, 0x57, 0xd2',
                                     widget=forms.Textarea(attrs={'cols': '48', 'rows': '8'}))





# -----------------------------------------------
    # request_bytes = forms.CharField(label='Запрос (request_bytes)', max_length=300)
    # response_bytes = forms.CharField(label='Ответ (response_bytes)', max_length=500)

    # request_bytes.widget.attrs.update(size='40')

