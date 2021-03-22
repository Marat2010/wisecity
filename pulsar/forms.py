from django import forms
from django.core.exceptions import ValidationError


class PulsarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PulsarForm, self).__init__(*args, **kwargs)
        print(f'+0++ INIT: {self.data.dict()}')
        print(f'++1+ INIT: {self.initial}')
        print(f'++ 2 + INIT: {self.fields["request_bytes"].initial}')

        # self.fields["request_bytes"].initial = self.initial
        # self.fields["request_bytes"].initial = self.initial['initial']
        self.fields["request_bytes"].initial = self.initial

        self.fields["request_bytes"].label = self.initial
        # self.fields["request_bytes"].empty_label = self.initial
        print(f'++ 3 + INIT: {self.fields["request_bytes"].initial}')
        print(f'+++4 INIT: {self.data.dict()}')

    # def get_initial(self):
    #     if not self.initial:
    #         self.initial = '0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,' \
    #                        ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73'
    #     return self.initial

    # forms.CharField.

    request_bytes = forms.CharField(label='Запрос (request_bytes) необязательно',
                                    required=False,
                                    initial='0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,'
                                            ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73',

    # initial=get_initial(),
                                    # # '0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,'
                                    # #         ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73',
                                    widget=forms.Textarea(attrs={'cols': '48', 'rows': '2'})
                                    )
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

    # request_bytes.widget.attrs.update(initial='sdadsd')
    # request_bytes.initial = '========req_by___ini '

    # initail = forms.CharField.__init__(initial=forms['request_bytes'])


        # self.fields['answer'].label = self.instance.question  # change required label ... and answers
        # self.fields['request_bytes'].initial = self.fields.initial['initial']   # ---
        # self.fields['answer'].queryset = Test.objects.get(question=self.instance.question).answers.all()
        # self.fields['answer'].empty_label = None


class PulsarForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PulsarForm2, self).__init__(*args, **kwargs)
        print(f'+0++ INIT: {self.data.dict()}')
        print(f'++1+ INIT: {self.initial}')
        print(f'++ 2 + INIT: {self.fields["request_bytes"].initial}')

        # self.fields["request_bytes"].initial = self.initial
        # self.fields["request_bytes"].initial = self.initial['initial']
        self.fields["request_bytes"].initial = self.initial

        self.fields["request_bytes"].label = self.initial
        # self.fields["request_bytes"].empty_label = self.initial
        print(f'++ 3 + INIT: {self.fields["request_bytes"].initial}')
        print(f'++ 3-5 + INIT: {self.fields["request_bytes"]}')
        print(f'+++4 INIT: {self.data.dict()}')
        print(f'+++5 INIT: {self.data.__dir__()}')
        # if self.data.POST:
        #     self.data["request_bytes"] = self.initial


    # def get_initial(self):
    #     if not self.initial:
    #         self.initial = '0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,' \
    #                        ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73'
    #     return self.initial

    # forms.CharField.

    request_bytes = forms.CharField(label='Запрос (request_bytes) необязательно',
                                    required=False,
                                    initial='0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,'
                                            ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73',

    # initial=get_initial(),
                                    # # '0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0xfc, 0x3f,'
                                    # #         ' 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73',
                                    widget=forms.Textarea(attrs={'cols': '48', 'rows': '2'})
                                    )
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

    # request_bytes.widget.attrs.update(initial='sdadsd')
    # request_bytes.initial = '========req_by___ini '

    # initail = forms.CharField.__init__(initial=forms['request_bytes'])


        # self.fields['answer'].label = self.instance.question  # change required label ... and answers
        # self.fields['request_bytes'].initial = self.fields.initial['initial']   # ---
        # self.fields['answer'].queryset = Test.objects.get(question=self.instance.question).answers.all()
        # self.fields['answer'].empty_label = None


# -----------------------------------------------
    # request_bytes = forms.CharField(label='Запрос (request_bytes)', max_length=300)
    # response_bytes = forms.CharField(label='Ответ (response_bytes)', max_length=500)

    # request_bytes.widget.attrs.update(size='40')

