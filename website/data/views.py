import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .scripts.biblioteca import construct_library

my_library = None
dataset_path = "data/datasets/fc_dataset.csv"


def make_list(x):
    if type(x) is not list:
        return [x]
    else:
        return x


def new(request):
    global my_library
    if my_library is None:
        my_library = construct_library(dataset_path)

    return HttpResponse(json.dumps(my_library))


@csrf_exempt
def update(request):
    if request.method == 'POST':
        # print(str(request.body))

        my_response = construct_library(dataset_path)

        profile = json.loads(request.body)
        bypass = {
            "gender": "any_gender",
            "race_ethnicity": "any_race",
            "employment": "any_employment",
            "age": "any_age_group",
            "marital_status": "any_marital_status",
            "sexual_orient": "any_orientation",
            "beliefs": "any_beliefs",
            "criminality": "any_criminal_status",
            "citizenship": "any_citizenship_status",
            "time_period": "either"
        }

        if 'All' not in profile['category']:
            seta = set(profile['category'])
            setb = set(my_response.keys())
            for cat in list(setb.difference(seta)):
                my_response.pop(cat)

        for k, v in profile.items():
            if k == 'category':
                continue

            for cat in list(my_response.keys()):
                for resource in my_response[cat]['data']:
                    if bypass.get(k, None) in v:
                        continue
                    else:
                        bools = list(map(lambda x: x in v, make_list(resource[k])))

                        if not any(bools) and k is not "time_period":
                            my_response[cat]['data'].remove(resource)

        return HttpResponse(json.dumps(my_response))
    else:
        return HttpResponse("Make a POST request, not {}.".format(request.method))
