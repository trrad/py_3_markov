from itertools import islice

def make_n_grams(iter, n):
    offset_lists = (islice(iter,i,None) for i in range(n)) #creates a tuple of input iterable offset by 1 through n
    return zip(*offset_lists) # here we unpack that tuple and zip it back up into a list of n-grams


with open('countries.txt','r') as file:
    #n_gram_list = [make_n_grams(line,4) for line in file]

    ngram_list = []
    for line in file:
        for ngram in make_n_grams(line,4):
            ngram_list.append(ngram)

print(len(ngram_list))
print(ngram_list)