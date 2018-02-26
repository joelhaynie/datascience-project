import csv

# list of important keywords associated with the candidate names
KEYWORD_IDENTIFIERS = ["said", "Dr.", "Ph.D.", "PE", "president", "CEO"]


def check_suffix_salutations():
    """checks if the candidate name has any suffix salutations"""
    check_suffix_salutation = 0
    names = name.split()
    suffix_salutations = ["Jr.", "Sr.", "I", "II", "III", "IV"]
    for salutation in suffix_salutations:
        if salutation in names:
            check_suffix_salutation = 1
    return check_suffix_salutation


def minimum_distance_to_period():
    """finds the minimum distance to period for the candidate name"""
    period_locations = []
    period_location = -1

    # populate the period locations array
    while True:
        period_location = file_contents.find(".", period_location + 1)
        if period_location == -1:
            break

        period_locations.extend([period_location])

    # find the location of the closet period from the start or end position
    min_location_of_period = -1
    for p in period_locations:
        if min_location_of_period == -1 or abs(start_position - p) < min_location_of_period:
            min_location_of_period = p

        if min_location_of_period == -1 or abs(end_position - p) < min_location_of_period:
            min_location_of_period = p

    return min_location_of_period


def minimum_distance_to_keywords():
    """finds the minimum distance to important keywords for the candidate name"""
    location_of_closed_keyword = -1

    # find the location of the closest keyword from the start or end position
    for keyword in KEYWORD_IDENTIFIERS:
        keyword_location = -1
        while True:
            keyword_location = file_contents.find(keyword, keyword_location + 1);
            if keyword_location == -1:
                break
            if location_of_closed_keyword == -1 or abs(keyword_location - start_position) < location_of_closed_keyword:
                location_of_closed_keyword = keyword_location;

            if location_of_closed_keyword == -1 or abs(keyword_location - end_position) < location_of_closed_keyword:
                location_of_closed_keyword = keyword_location;

    return location_of_closed_keyword;


with open('internediatefeaturespace.csv', 'r') as intermediateFeaturesFile:
    intermediateFeatureReader = csv.DictReader(intermediateFeaturesFile)
    fieldnames = ['id', 'name', 'some_capitalized', 'atleast_one_capitalized', 'first_letter_capitalized',
                  'has_suffix_salutation', 'start_position', 'distance_to_period', 'distance_to_closest_keyword',
                  'frequency', 'label']
    output = csv.DictWriter(open("featurespace.csv", "w"), fieldnames=fieldnames)
    output.writeheader()

    for row in intermediateFeatureReader:
        identifier = row['Id']
        name = row['name']
        some_capitalized = 1 if sum(1 for c in name if c.isupper()) > 2 else 0
        atleast_one_capitalized = 1 if sum(1 for c in name if c.isupper()) >= 1 else 0
        first_letter_capitalized = 1 if name[0].isupper() else 0
        has_suffix_salutations = check_suffix_salutations()
        start_position = int(row['start_position'])
        end_position = int(row['end_position'])
        label = row['label']
        frequency = row['frequency']

        file_name = row['file_name'];
        reference_file = open(file_name, 'r');
        file_contents = reference_file.read();

        min_distance_to_period = minimum_distance_to_period();
        min_distance_to_key_words = minimum_distance_to_keywords();

        output.writerow({'id': identifier,
                         'name': name,
                         'some_capitalized': some_capitalized,
                         'atleast_one_capitalized': atleast_one_capitalized,
                         'first_letter_capitalized': first_letter_capitalized,
                         'has_suffix_salutation': has_suffix_salutations,
                         'start_position': start_position,
                         'distance_to_period': min_distance_to_period,
                         'distance_to_closest_keyword': min_distance_to_key_words,
                         'frequency': frequency,
                         'label': label});