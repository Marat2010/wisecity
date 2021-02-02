from django import forms


class PulsarForm(forms.Form):
    request_bytes = forms.CharField(label='Запрос (request_bytes)', max_length=300)
    response_bytes = forms.CharField(label='Ответ (response_bytes)', max_length=300)
