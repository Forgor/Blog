
def mystery1(wordlist):
    scored_words = [[w[-1], w] for w in wordlist]
    print(scored_words)
    best_pair = max(scored_words)
    return best_pair[1]

print(mystery1(['do','you','comprehend','this']))
