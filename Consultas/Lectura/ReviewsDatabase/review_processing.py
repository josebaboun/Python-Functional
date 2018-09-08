def clean_reviews(reviews):
    for review in reviews:
        review = _clean_reviews(review)
        yield review


def _clean_reviews(review):
    "quita signos a los reviews para analizar palabras correctamente"
    review_str = review["review"]
    review_str = review_str.replace(".", " ").replace("\"", " ")
    review_str = review_str.replace("\\", " ").replace("\'", " ")
    review_str = review_str.replace("!", " ").strip()
    review_str = review_str.split()
    review_str = " ".join(review_str)
    review["review"] = review_str
    return review


def filter_words(words, filter):
    words = [word[0] for word in words if word[1] == filter]
    return words


def count_words(review, words):
    review = review["review"].split()
    review = [word for word in review if word in words]
    return len(review)


def check_review(review, words):
    positive_words = count_words(review, filter_words(words, "positive"))
    negative_words = count_words(review, filter_words(words, "negative"))
    total_words = len(review)
    return review_status(positive_words, negative_words, total_words)


def review_status(positive, negative, total):
    positive_cond = positive/total >= 0.6 and negative/total <= 0.2
    negative_cond = negative/total >= 0.6 and positive/total <= 0.2
    if positive/total >= 0.8 or positive_cond:
        return "positive"
    elif negative/total >= 0.8 or negative_cond:
        return "negative"
    else:
        return "neutral"
