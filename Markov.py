class Markov:
    """
    A data structure that represents a Tri-Gram Markov model by using three dictionaries

    '''
    Methods
    -------
    tri_gram_probability(third_word, given_first_word, given_second_word):
        computes the probability of the third word, given the first and second word

    put_words(first_word, second_word, third_word):
        puts all three words into the Tri-Gram Markov model

    """

    def __init__(self):
        self.model = {}

    def __getitem__(self, item):
        return self.model[item]

    def __setitem__(self, key, value):
        self.model[key] = value

    def __contains__(self, item):
        return item in self.model

    def __iter__(self):
        return iter(self.model)

    def keys(self):
        return self.model.keys()

    def highest_bi_gram(self, first_word):
        """
        Finds the bi-gram with the highest probability given the first word
        :param first_word: The first word
        :return: The most likely second word
        """
        highest = 0
        for word in self[first_word]:
            probability = self.bi_gram_probability(word, first_word)
            if highest < probability:
                highest = probability
                highest_word = word
        return highest_word

    def highest_tri_gram(self, first_word, second_word):
        highest = 0
        for word in self[first_word][second_word]:
            probability = self.tri_gram_probability(word, first_word, second_word)
            if highest < probability:
                highest = probability
                highest_word = word
        return highest_word

    def bi_gram_probability(self, second_word, given_first_word):
        """
        Computes the probability of the second word given the first word by dividing
        the total number of times the sequence (first then second word) was found by the number of
        words found after the first word

        :param second_word:
        :param given_first_word:
        :return:
        """

        if second_word in self[given_first_word]:
            return self[given_first_word][second_word].count / self[given_first_word].get_total_next_words()
        else:
            return 0

    def tri_gram_probability(self, third_word, given_first_word, given_second_word):
        """
        Computes the probability of the third word given the first and second word
        by dividing the total number of times the sequence (first, then second, then third word) was
        found by the number of words found after the first and second word
        P(third_word | given_first_word, given_second_word)

        :param third_word: str The word to compute the probability of
        :param given_first_word: str The given first word
        :param given_second_word: str The given second word
        :return: a decimal representing the probability
        """
        if third_word in self[given_first_word][given_second_word]:
            return self[given_first_word][given_second_word][third_word].count / self[given_first_word][
                given_second_word].get_total_next_words()
        else:
            return 0

    def put_words(self, first_word, second_word, third_word):
        """
        Puts all three words into the Markov data structure

        :param first_word: The first word to put
        :param second_word: The second word to put
        :param third_word: The third word to put
        :return:
        """
        self._put_first_word(first_word)
        self._put_second_word(first_word, second_word)
        self._put_third_word(first_word, second_word, third_word)

    def _put_first_word(self, word):
        if word in self:  # we've found this word before, so update its count
            self[word].count += 1
        else:  # it's a new word
            self[word] = Word(word)

    def _put_second_word(self, first_word, second_word):
        if second_word in self[first_word]:  # we've found this word before, so update its count
            self[first_word][second_word].count += 1
        else:  # it's a new word
            self[first_word][second_word] = Word(second_word)

    def _put_third_word(self, first_word, second_word, third_word):
        if third_word in self[first_word][second_word]:  # we've found this word before, so update its count
            self[first_word][second_word][third_word].count += 1
        else:  # it's a new word
            self[first_word][second_word][third_word] = Word(third_word)


class Word:
    """
    A word in the Tri-gram Markov model, contains a word a count, and a dictionary
    of the next words in the sequence

    '''
    Methods
    -------
    keys():
        :returns: The keys in the dictionary of next words
    """

    def __init__(self, value, count=1):
        """

        :param value: str
                        The string value of the word
        :param count: default 1
                        The number of times the word has been found
        """
        self.value = value
        self.count = count
        self.next_words = {}

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __getitem__(self, item):
        return self.next_words[item]

    def __setitem__(self, key, value):
        self.next_words[key] = value

    def __iter__(self):
        return iter(self.next_words)

    def __contains__(self, item):
        return item in self.next_words

    def keys(self):
        """
        :return: The keys in the dictionary of next words
        """
        return self.next_words.keys()

    def get_total_next_words(self):
        """
        Adds up all the count values of the Word objects in the next words dictionary
        :return: The total number of Words found in the dictionary
        """
        count = 0

        for key in self:
            count += self[key].count

        return count
