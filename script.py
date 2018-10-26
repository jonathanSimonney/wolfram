import numpy
from flask import Flask
app = Flask(__name__)


result_array = numpy.zeros((40, 79), dtype=int)


def get_cell_number_getter(rule_number):
    wolfram_rule = bin(rule_number)

    array_rule = [int(d) for d in str(wolfram_rule)[2:]]

    while len(array_rule) < 8:
        array_rule.insert(0, 0)

    corr_array = {
        "111": array_rule[0],
        "110": array_rule[1],
        "101": array_rule[2],
        "100": array_rule[3],
        "011": array_rule[4],
        "010": array_rule[5],
        "001": array_rule[6],
        "000": array_rule[7],
    }

    def get_cell_number(y, x):
        first_number = result_array[y - 1, x - 1] if x - 1 >= 0 else 0
        second_number = result_array[y - 1, x]
        third_number = result_array[y - 1, x + 1] if x + 1 <= 78 else 0
        array_key = str(first_number) + str(second_number) + str(third_number)
        return corr_array[array_key]

    return get_cell_number


def get_str_to_display(rule_number):
    get_cell_number = get_cell_number_getter(rule_number)

    result_array[0, 39] = 1

    for y in range(39):
        for x in range(79):
            result_array[y + 1, x] = get_cell_number(y + 1, x)

    buffer = []
    for y in range(40):
        str_to_display = ""
        for x in range(79):
            if result_array[y, x] == 1:
                str_to_display += "#"
            else:
                str_to_display += "."
        buffer.append(str_to_display)

    final_str_to_display = '\n'.join(buffer)
    return final_str_to_display


# parser = argparse.ArgumentParser(description='Gives a wolfram representation made of # and . with the parameter number')
# parser.add_argument('rule_number', metavar='rule', type=int,
#                     help='an integer for the wolfram rule')
#
# args = parser.parse_args()
# print(get_str_to_display(args.rule_number))


@app.route("/<int:rule_number>")
def hello(rule_number):
    return '<pre>' + get_str_to_display(rule_number) + '</pre>'

