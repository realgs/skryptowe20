def summaries_to_json(currency, summaries):
    json = ("{\"currency\":"
            f"\"{currency}\","
            "\"data\":[")
    for summary in summaries:
        json += ("{\"date\":"
                 f"\"{summary[0]}\","
                 "\"original_sum\":"
                 f"\"{summary[1]}\","
                 "\"currency_sum\":"
                 f"\"{summary[2]}\""
                 "},")
    json=json[:-1]
    json += "]}"
    return json
