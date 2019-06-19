
import re


NOT_FOUND_SCORE = -1
NO_SCORE = 0


def get_search_regex(query, ignore_case=True):

    regex_text = [char for char in query if char != ' ']
    regex_text = '.*'.join(regex_text)

    regex = r'({0})'.format(regex_text)

    if ignore_case:
        pattern = re.compile(regex, re.IGNORECASE)
    else:
        pattern = re.compile(regex)

    return pattern


def get_search_score(query, choice, ignore_case=True, apply_regex=True,
                     template='{}'):
  

    original_choice = choice
    result = (original_choice, NOT_FOUND_SCORE)

    # Handle empty string case
    if not query:
        return result

    if ignore_case:
        query = query.lower()
        choice = choice.lower()

    if apply_regex:
        pattern = get_search_regex(query, ignore_case=ignore_case)
        r = re.search(pattern, choice)
        if r is None:
            return result
    else:
        sep = u'-'  # Matches will be replaced by this character
        let = u'x'  # Nonmatches (except spaed) will be replaced by this
        score = 0

        exact_words = [query == word for word in choice.split(u' ')]
        partial_words = [query in word for word in choice.split(u' ')]

        if any(exact_words) or any(partial_words):
            pos_start = choice.find(query)
            pos_end = pos_start + len(query)
            score += pos_start
            text = choice.replace(query, sep*len(query), 1)

            enriched_text = original_choice[:pos_start] +\
                template.format(original_choice[pos_start:pos_end]) +\
                original_choice[pos_end:]

        if any(exact_words):
            # Check if the query words exists in a word with exact match
            score += 1
        elif any(partial_words):
            # Check if the query words exists in a word with partial match
            score += 100
        else:
            # Check letter by letter
            text = [l for l in original_choice]
            if ignore_case:
                temp_text = [l.lower() for l in original_choice]
            else:
                temp_text = text[:]

            # Give points to start of string
            score += temp_text.index(query[0])

            # Find the query letters and replace them by `sep`, also apply
            # template as needed for enricching the letters in the text
            enriched_text = text[:]
            for char in query:
                if char != u'' and char in temp_text:
                    index = temp_text.index(char)
                    enriched_text[index] = template.format(text[index])
                    text[index] = sep
                    temp_text = [u' ']*(index + 1) + temp_text[index+1:]

        enriched_text = u''.join(enriched_text)

        patterns_text = []
        for i, char in enumerate(text):
            if char != u' ' and char != sep:
                new_char = let
            else:
                new_char = char
            patterns_text.append(new_char)
        patterns_text = u''.join(patterns_text)
        for i in reversed(range(1, len(query) + 1)):
            score += (len(query) - patterns_text.count(sep*i))*100000

        temp = patterns_text.split(sep)
        while u'' in temp:
            temp.remove(u'')
        if not patterns_text.startswith(sep):
            temp = temp[1:]
        if not patterns_text.endswith(sep):
            temp = temp[:-1]

        for pat in temp:
            score += pat.count(u' ')*10000
            score += pat.count(let)*100

    return original_choice, enriched_text, score


def get_search_scores(query, choices, ignore_case=True, template='{}',
                      valid_only=False, sort=False):
    

    query = query.replace(' ', '')
    pattern = get_search_regex(query, ignore_case)
    results = []

    for choice in choices:
        r = re.search(pattern, choice)
        if query and r:
            result = get_search_score(query, choice, ignore_case=ignore_case,
                                      apply_regex=False, template=template)
        else:
            if query:
                result = (choice, choice, NOT_FOUND_SCORE)
            else:
                result = (choice, choice, NO_SCORE)

        if valid_only:
            if result[-1] != NOT_FOUND_SCORE:
                results.append(result)
        else:
            results.append(result)

    if sort:
        results = sorted(results, key=lambda row: row[-1])

    return results


