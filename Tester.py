import random
import string

from Markov import Markov

FILES = ["houn.txt", "sign.txt", "stud.txt", "vall.txt"]
FILES_TO_CONSUME = 4
STORY_LENGTH = 2000

# the titles of each story stored in strings, used to skip the title, author and chapter name
TITLES = [
    """
                          THE HOUND OF THE BASKERVILLES

                               Arthur Conan Doyle
          CHAPTER I
          Mr. Sherlock Holmes

""",
    """                              THE SIGN OF THE FOUR

                               Arthur Conan Doyle

          CHAPTER I
          The Science of Deduction

""",
    """
                               A STUDY IN SCARLET

                               Arthur Conan Doyle
          CHAPTER I
          Mr. Sherlock Holmes

""",
    """
                               THE VALLEY OF FEAR

                               Arthur Conan Doyle
    CHAPTER I
          The Warning

"""
]


def main():
    markov = Markov()
    for i in range(FILES_TO_CONSUME):  # training the tri-gram markov model
        file = open(FILES[i], "r")
        # remove the title, author name, chapter, and the line following it, then
        # convert the file to lowercase and consume it into the markov tri-gram model
        markov = consume_file_contents(markov, file.read().split(TITLES[i])[1].lower())
        file.close()
    # the model is trained, now generate the story
    readme = open("Readme.txt", "w")
    generate_new_story(markov, STORY_LENGTH, readme)
    readme.close()


def consume_file_contents(markov, file_contents):
    """
    Consumes the passed file contents into the passed markov tri-gram model
    by splitting the file contents by sentences and removing all punctuation from each sentence

    :param markov: The markov tri-gram model
    :param file_contents: The file contents
    :return: The markov tri-gram model
    """
    sentences = file_contents.split(".")

    for sentence in sentences:
        sentence = sentence.translate(
            str.maketrans('', '', string.punctuation)).strip()  # remove punctuation and whitespace from the sentence
        words = sentence.split()
        for i in range(len(words) - 2):
            # consume a three word sequence into the markov model
            markov.put_words(words[i], words[i + 1], words[i + 2])
    return markov


def generate_new_story(markov, story_length, file):
    """
    Generates a new story using the provided tri-gram markov model, the story length and the file to output to
    (the story may be a few characters longer than the story length because it is generated every three words)
    :param markov: A trained tri-gram markov model
    :param story_length: The length the story should be
    :param file: The file to output the story to
    """
    first_word = get_random_first_word(markov)
    word_count = 0
    sequences_used = []  # stores all the sequences we've used so far

    while word_count < story_length:
        sequence = generate_new_sequence(markov, first_word)
        if sequence in sequences_used:
            # we've already used this sequence so get a new sequence with a random first word
            sequence = generate_new_sequence(markov, get_random_first_word(markov))
        sequences_used.append(sequence)
        file.write(sequence)
        if word_count >= 24 and word_count % 24 == 0:  # insert a newline every 24 words
            file.write("\n")
        word_count += 3
        sequence = sequence.split()
        second_word = sequence[1]
        third_word = sequence[2]
        if third_word in markov:  # if the third word is in the dictionary of first words
            # the next first word is the highest bi-gram after the third word
            first_word = markov.highest_bi_gram(third_word)
        elif second_word in markov:  # the third word wasn't in the dictionary so check for the second word
            # the next first word is the highest bi-gram after the second word (the third word)
            first_word = third_word
        else:  # the third and second words aren't in the dictionary so get a first word at random
            first_word = markov.highest_bi_gram(get_random_first_word(markov))


def generate_new_sequence(markov, first_word):
    """
    Creates a new three word sequence given a tri-gram markov model and the first word in the sequence.
    If the first word is not a valid key in the first word dictionary of the markov model it will get a
    new random first word in the first word dictionary of the markov model
    :param markov: The trained tri-gram markov model
    :param first_word: The first word in the three word sequence
    :return: The three word sequence
    """
    if first_word not in markov:  # the first_word is invalid so get a random first word
        first_word = get_random_first_word(markov)
    second_word = markov.highest_bi_gram(first_word)
    third_word = markov.highest_tri_gram(first_word, second_word)
    return first_word + " " + second_word + " " + third_word + " "


def get_random_first_word(markov):
    """
    Gets a random word in the first word dictionary of the passed tri-gram markov model
    :param markov: The tri-gram markov model
    :return: A random word from the first word dictionary in the tri-gram markov model
    """
    return random.choice(list(markov.keys()))


if __name__ == "__main__":
    main()
