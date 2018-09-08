def remove_bot_reviews(reviews, vocabulary):
    reviews = filter(lambda review: not_bot_review(review, vocabulary),
                     reviews)
    for review in reviews:
        yield review


def not_bot_review(review, vocabulary):
    review = review["review"].split()
    if _review_lenght(review) and _bot_vocabulary(review, vocabulary):
        return False
    else:
        return True


def _review_lenght(review):
    if len(review) <= 64 and len(review) >= 8:
        return True
    else:
        return False


def _bot_vocabulary(review, vocabulary):
    vocabulary = list(vocabulary)
    review = [word for word in review if word in vocabulary]
    if words_repited(review) and len(review) >= 4:
        return True
    else:
        return False


def words_repited(review):
    for word in review:
        if review.count(word) >= 3:
            return True
    return False
