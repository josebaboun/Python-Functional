def remove_tags(reviews):
    for review in reviews:
        # if "<" in review[1]:
        review["review"] = remove_tags_string(review["review"])
        yield review


def remove_tags_string(string):
    string = string.split("<")
    string = [data.split(">") for data in string]
    if len(string[0]) == 1:
        return _remove_tags_string(string[0], string[1:])
    else:
        return _remove_tags_string(None, string[1:])


def _remove_tags_string(head, string):
    string = [data[1] for data in string if len(data) > 1]
    if head:
        return str(head) + "".join(string)
    else:
        return "".join(string)
