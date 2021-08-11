"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    true_choose = []
    for i in paragraphs:
        if select(i):
            true_choose.append(i)

    if len(true_choose) <= k:
            return ''

    return true_choose[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def topic_in_paragraph(paragraph):
        remove = remove_punctuation(paragraph)
        low = lower(remove)
        split_para = split(low)
        for i in split_para:
            if i in topic:
                return True
        return False
    return topic_in_paragraph
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    correct_words, max_index = 0, min(len(typed_words), len(reference_words))

    if max_index == 0:
        return 0.0

    for i in range(max_index):
        if typed_words[i] == reference_words[i]:
            correct_words += 1

    return correct_words / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return 60 * len(typed) / (5 * elapsed)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word

    d = {}
    for word in valid_words:
        difference = diff_function(user_word, word, limit)
        d[word] = difference

    min_word = min(d, key=d.get)

    if d[min_word] <= limit:
        return min_word
    else:
        return user_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """

    if goal == "":
        if len(start) <= limit:
            return len(start)
        else:
            return limit+1

    if start == "":

        if len(goal) <= limit:
            return len(goal)
        else:
            return limit+1

    if start[0] == goal[0]:
        return swap_diff(start[1:],goal[1:], limit)
    if limit == 0:
        return 1

    if start[0] != goal[0]:
        return 1+swap_diff(start[1:],goal[1:], limit-1)

    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    def helper(start, counter, index):

        if counter>limit:
            return counter+1

        if index>=len(start) or index>=len(goal):
            return counter+abs(len(start)-len(goal))

        def remove():
            newStart = start[:index]+start[index+1:]
            return newStart
        def add():
            newStart = start[:index]+goal[index]+start[index:]
            return newStart
        def replace():
            newStart = start[:index]+goal[index]+start[index+1:]
            return newStart

        if(start[index]==goal[index]):
            return helper(start, counter, index+1)
        else:
            return min(helper(add(), counter+1, index+1), helper(remove(), counter+1, index), helper(replace(), counter+1, index+1))



    return helper(start, 0, 0)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    index = 0
    progress = 0

    while index < len(typed):
        if typed[index] !=  prompt[index]:
            progress = index/len(prompt)
            index = len(typed)
            data =	{
              'id': id,
              'progress': progress
            }
            send(data)
            return progress
        index = index+ 1

    progress = len(typed)/len(prompt)
    data =	{
      'id': id,
      'progress': progress
    }
    send(data)

    return progress

    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    fastestTyped=[]
    for player in word_times: # 3 empty lists, one for each player
        fastestTyped.append([])


    players = len(word_times)
    numberOfWords = len(word_times[0])
    for wordIndex in range(1, numberOfWords):
        minValue = -1

        for playerIndex in range(players):
            difference = elapsed_time(word_times[playerIndex][wordIndex]) - elapsed_time(word_times[playerIndex][wordIndex-1])
            if minValue == -1 or difference < minValue:
                minValue = difference

        for playerIndex in range(players):
            difference = elapsed_time(word_times[playerIndex][wordIndex]) - elapsed_time(word_times[playerIndex][wordIndex-1])
            if difference <= minValue+margin and difference >= minValue-margin:
                fastestTyped[playerIndex].append(word(word_times[playerIndex][wordIndex]))

    return fastestTyped

    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
