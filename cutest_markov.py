class Chain:

    def __init__(self,corpus,ngram_size=3):
        self.ngram_size = ngram_size
        self.begin_states = []

        ngrams = self.n_gramify_file(corpus,ngram_size)
        self.chain = self.build_markov_chain(ngrams)

    def make_n_grams(self,iter, n):
        """Here we create a tuple of the the input iterable offset by 1 through n.
        We then zip up these offset iterables to create the desired n-grams."""
        offset_lists = (islice(iter,i,None) for i in range(n))
        return zip(*offset_lists)

    def n_gramify_file(self,file,n):
        """Simple helper function to load ngrams in from a file."""
        with open(file,'r') as file:
            for line in file:
                    yield self.make_n_grams(line,n)

    def build_markov_chain(self,ngrams):
        """Here we build a dict of dicts that represents our markov chain.
            - top level keys are all possible states
            - 2nd level keys are the possible predictions for each state.
            - values stored are a count of prediction frequency in text corpus
         """
        model = {}
        for ngram_list in ngrams:
            for i, ngram in enumerate(ngram_list):
                state = ngram[:-1] #state is all but the last item
                if i == 0: #append first ngram to valid begin states list
                    self.begin_states.append(state)
                prediction = ngram[-1] #prediction is the last item

                if state not in model:
                    model[state] = {}

                if prediction not in model[state]:
                    model[state][prediction] = 0

                model[state][prediction] += 1
        return model

    def predict(self,state):
        """Chooses the prediction given the state, using the frequency
        of occurrence to determine it's chance."""
        offset = random.randint(0, sum(iter(self.chain[state].values())) - 1)
        for key, value in iter(self.chain[state].items()):
            if offset < value:
                return key
            offset -= value

    def generate(self,begin_state=None):
        """This returns a generator that will iterate through a walk down
        the chain given an initial state (if not provided will be chosen randomly
        from valid begin_states).
        """
        if begin_state == None:
            state = random.choice(self.begin_states)
        else:
            state = begin_state
            if state not in self.chain.keys():
                raise KeyError('Provided begin_state not found in model.')

        while state in self.chain.keys():
            prediction = self.predict(state)
            last_state = state
            state = state[1:] + tuple(prediction)
            yield last_state, prediction
