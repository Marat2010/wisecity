from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import PulsarForm
from .task import parse_response
import json


def pulsar(request):
    if request.method == 'POST':
        form = PulsarForm(request.POST)
        if form.is_valid():
            request_bytes = form.data['request_bytes']
            response_bytes = form.data['response_bytes']

            print(f"--- Запрос request_bytes --- {request_bytes}")
            print(f"--- Ответ response_bytes --- {response_bytes}")

            data_error = False
            result = ''
            try:
                response_bytes = [int(i, 16) for i in response_bytes.split(',') if i != '']
                result = parse_response(bytearray(response_bytes))
            except ValueError:
                data_error = True
            print(f"---result----: {json.dumps(result, indent=4, sort_keys=True)}")

            context = {'form': form, 'result': result, 'data_error': data_error}
            return render(request, 'pulsar/index.html', context=context)
    else:
        form = PulsarForm()

    return render(request, 'pulsar/index.html', {'form': form})


# -------------------------------------------------
    # request_bytes = bytearray([0x02, 0x27, 0x21, 0x35, 0x01, 0x0e, 0xfc, 0x3f, 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73])
    # response_bytes = bytearray([
    #     0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0x95, 0x13, 0x61, 0x42, 0xc3, 0x5b, 0x36, 0x42, 0x48, 0xdf, 0x2a, 0x41,
    #     0x81,
    #     0x36, 0x1e, 0x3b, 0x37, 0xd1, 0x80, 0x41, 0x89, 0x3b, 0xc1, 0x44, 0x66, 0x30, 0x6a, 0x3e, 0xff, 0xff, 0xff,
    #     0xff,
    #     0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc7, 0x3f, 0x6a, 0x3e, 0x6c, 0x2d,
    #     0x00,
    #     0x00, 0xba, 0x1c, 0x57, 0xd2 ])


