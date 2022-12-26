# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
# Name - Mansi Kishore Ranka, Tanmay Girish Mahindrakar, Sohan Narayan Kakatkar
# UID: mranka, tmahind, skakatka
#
# Based on skeleton code by D. Crandall, October 2021
#

## TODO -> Think how to imporve accuracy(treat misspellings, remove punctuations, remove numbers, don't consider occurances of low probability)
## TODO -> NOTE -> Out of the misclassified text the truthful misclassified ones are 43 while deceptive misclassified ones are 18. It is always better to be careful
## Hence the truthful ones should not be misclassified to such a great extent
## TODO -> Analyze the misclassified sentences better
from multiprocessing.spawn import is_forking
import sys
import string
import math
# import matplotlib.pyplot as plt
from typing import Set
# from sklearn.model_selection import train_test_split


def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

## The python syntax for removing punctuation was taken from geeks for geeks -> https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
## Step 1: removing punctuation from words -> this increasesd the accuracy from 76.18% to 77%
## Step 2: after Step 1 I removed numbers from string -> accuracy decreased from 77% to 76.50%
## Step 3: after Step 2 I took log of probabilities -> accuracy increased from 77% to 80%
## Step 4: after Step 3 I removed stop words -> accuracy increased to 84%
## Step 5: after Step 4 I removed the s at the end of the word and removed the numbers as well in string. Accuracy improved to 85%
## Step 6: after Step 5 I replaced dont with don't and didnt with didn't and im with in -> accuracy improved to 85.50% 
## Treating misspellings -> TODO Not sure how to do that(Research on this)
def process_string(str):
    true_words = {"dont":"don't","didnt":"didn't","in": "im","reccomend":"recommended","prolem":"problem","couldnt":"couldn't","quieted":"quite","everythingcomplete":"everything complete"}
    #str = ''.join([i for i in str if not i.isdigit()])
    processed_str = str.translate(str.maketrans('', '', string.punctuation))

    # stop_words = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "for", "who", 
    #             "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don't", "nor", "me", "were", "her", 
    #             "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", 
    #             "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", 
    #             "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"}
    stop_words = {"0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"}
    word_list_temp = processed_str.split()
    word_list = []

    for word in word_list_temp:
        if (true_words.get(word,None)!=None):
            word_list.append(true_words[word])
        else:
            word_list.append(word)
    
    processed_words_list = [w.lower() for w in word_list if not w.lower() in stop_words]
    processed_words_list = [word if(word[-1]!='s') else word[:-1] for word in processed_words_list]
    return processed_words_list

def get_probability(data,label,category):
    prob_dict_a,prob_dict_b= {},{}

    total_words_a,total_words_b = 0,0
    total_vocabulary = set()

    for i,str in enumerate(data):
        d = process_string(str)
        if(label[i]==category):
            words_list = d
            #words_list = d.split()
            total_words_a = total_words_a+len(words_list)
            for word in words_list:
                lower_word = word.lower()
                total_vocabulary.update(lower_word)
                if(prob_dict_a.get(lower_word)==None):
                    prob_dict_a[lower_word]=1
                else:
                    prob_dict_a[lower_word] = prob_dict_a[lower_word]+1
        else:
            words_list = d
            #words_list = d.split()
            total_words_b = total_words_b+len(words_list)
            for word in words_list:
                lower_word = word.lower()
                total_vocabulary.update(lower_word)
                if(prob_dict_b.get(lower_word)==None):
                    prob_dict_b[lower_word]=1
                else:
                    prob_dict_b[lower_word] = prob_dict_b[lower_word]+1
    
    for word in prob_dict_a:
        #prob_dict_a[word] = prob_dict_a[word]/total_words_a
        prob_dict_a[word] = math.log((prob_dict_a[word])/(total_words_a))

    for word in prob_dict_b:
        #prob_dict_b[word] = prob_dict_b[word]/total_words_b
        prob_dict_b[word] = math.log((prob_dict_b[word])/(total_words_b))
    return prob_dict_a,prob_dict_b

def predict(prob_a,prob_b,class_a,class_b,data,dict_a,dict_b):
    data = process_string(data)
    test_data = data
    #test_data = data.split()

    #ratio = prob_a/prob_b
    ratio = math.log(prob_a) - math.log(prob_b)

    for word in test_data:
        word = word.lower()
        #ratio = ratio*dict_a.get(word,0.00000001)/dict_b.get(word,0.00000001)
        ratio = ratio + dict_a.get(word,-10) - dict_b.get(word,-10)
    
    # if(ratio >1):
    #     return class_a

    if(ratio>0):
        return class_a
    return class_b

# def predict_validation(prob_a,prob_b,class_a,class_b,data,labels,dict_a,dict_b):
#     #test_data = data.split()

#     #ratio = prob_a/prob_b
#     ratio = math.log(prob_a) - math.log(prob_b)

#     error_log = []

#     min_log_size = [-100,-50,-20,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5]

#     for c in min_log_size:
#         count = 0
#         total_words = 0
#         ratio = 0
#         predict_labels = []

#         for i in range(len(data)):
#             single_str = process_string(data[i])
#             test_data = single_str
#             for word in test_data:
#                 total_words = total_words+1
#                 word = word.lower()
#                 #ratio = ratio*dict_a.get(word,0.00000001)/dict_b.get(word,0.00000001)
#                 ratio = ratio + dict_a.get(word,c) - dict_b.get(word,c)

#             if(ratio>0):
#                 predict_labels.append(class_a)
#             else:
#                 predict_labels.append(class_b)

#             if((ratio>0 and labels[i]==class_a) or (ratio<0 and labels[i]==class_b)):    
#                 count = count + 1
#             correct_ct = sum([ (predict_labels[i] == labels[i]) for i in range(0, len(labels)) ])
#             print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(labels)))

#         error_log.append(count)
    
    # # print("hi")
    # print(error_log)
    # plt.plot(min_log_size,error_log)
    # plt.show()
    
    # # if(ratio >1):
    # #     return class_a

    # if(ratio>0):
    #     return class_a
    # return class_b


# def split_data(x,y,class_a,class_b):

#     len_x = len(x)
#     #print(x[0:800])
#     # train_data = x[0:800]
#     # train_labels = y[0:800]

#     # #print(train_data)

#     # validation_data = x[800:]
#     # validation_labels = y[800:]

#     train_data, validation_data, train_labels, validation_labels = train_test_split(x,y,test_size=0.30)

#     prob_a,prob_b = train_labels.count(class_a)/len(train_labels),train_labels.count(class_b)/len(train_labels)

#     dict_a,dict_b = get_probability(train_data,train_labels,class_a)

#     validation_classes = []

#     predict_validation(prob_a,prob_b,class_a,class_b,validation_data,validation_labels,dict_a,dict_b)

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    class_a,class_b = train_data['classes']
    labels_train = train_data['labels']
    data_train = train_data['objects']

    # print(data_train[0])

    #split_data(data_train,labels_train,class_a,class_b)

    #return 0

    data_test = test_data["objects"]
    labels_test = test_data["classes"]
    #print(len(labels_test))

    # print(data_test[0])

    prob_a,prob_b = labels_train.count(class_a)/len(labels_train),labels_train.count(class_b)/len(labels_train)

    ## Evaluating the p(word|class_a)
    dict_a,dict_b = get_probability(data_train,labels_train,class_a)
    #print(dict_b)
    #dict_b = get_probability(data_train,labels_train,class_b)

    test_classes = []

    for t in data_test:
        test_classes.append(predict(prob_a,prob_b,class_a,class_b,t,dict_a,dict_b))

    return test_classes
    
    return [test_data["classes"][0]] * len(test_data["objects"])

def calculate_accuracy(predicted, true_labels, test_data):
    truthful_mispredict, deceptive_mispredict = 0,0

    truthful_misclassified, deceptive_misclassified = {},{}
    for i in range(len(predicted)):
        if(predicted[i]!=true_labels[i]):
            # print(true_labels[i],end = " ")
            # print(predicted[i])
            if(true_labels[i]=="deceptive"):
                deceptive_mispredict = deceptive_mispredict+1
                deceptive_misclassified[i] = test_data[i]
                #print(process_string(test_data[i]))
            else:
                truthful_mispredict = truthful_mispredict+1
                truthful_misclassified[i] = test_data[i]
                # print("HI")
                # print(process_string(test_data[i]))
    #print(truthful_mispredict,end = " ")
    #print(deceptive_mispredict)
    return deceptive_misclassified, truthful_misclassified

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    deceptive_misclassified, truthful_misclassified = calculate_accuracy(results,test_data["labels"],test_data_sanitized["objects"])

    # print(deceptive_misclassified)

    # print("----------------------------")

    # print(truthful_misclassified)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
