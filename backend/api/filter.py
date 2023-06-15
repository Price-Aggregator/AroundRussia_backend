def sort_by_time(sorted_obj):
    print(type(sorted_obj['data']))
    sorted_obj['data'].sort(key=lambda x: x["departure_at"])
    return sorted_obj
