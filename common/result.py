from bson.json_util import dumps


def SUCCESS(data="SUCCESS", **kwargs):
    result = {
        "code": 0,
        "data": data
    }
    if kwargs:
        result.update(kwargs)
    return dumps(result)


def ERROR(msg, code=1, **kwargs):
    result = {
        "code": code,
        "errorMessage": msg
    }
    if kwargs:
        result.update(kwargs)
    return dumps(result)
