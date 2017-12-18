from senti import CoinFeels, format_sentence

def get_payload(entry):
    payload = {}    
    if type(entry) is str:
        title = entry
        published = " "
    else:
        title = entry.title
        published = entry.published
    
    output = COIN.classifier.prob_classify(format_sentence(title))
    label = COIN.classifier.classify(format_sentence(title))
    ct = output.__dict__
    score = (ct['_prob_dict']['pos'] - ct['_prob_dict']['neg'])
    summary = {"date":published,"score":score,"label":label,"title":title}
    technical = {"tags":output.__dict__,"feats":format_sentence(title),"text":title}
    payload["summary"], payload["technical"] =  summary, technical
    return payload


print "\nDa manager is doing important Artificial Intelligence things\n"

COIN = CoinFeels("IOTA")
COIN.populate_articles()
COIN.train("./data/positive_articles.txt","./data/negative_articles.txt")


print "\nNow its done..\n"