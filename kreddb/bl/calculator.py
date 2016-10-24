import execjs
from django.contrib.staticfiles import finders


def calculate_interest_and_credit(price, first_payment, credit_length, no_insurance, no_confirmation, variation):
    js_calc_filename = 'kreddb/js/creditcalc/calculator.js'
    py_start_token = '// py_start'
    py_end_token = '// py_end'
    js_calc_filepath = finders.find(js_calc_filename)

    with open(js_calc_filepath) as js_calc_file:
        js_calc = js_calc_file.read()

    py_start = js_calc.index(py_start_token) + len(py_start_token)
    py_end = js_calc.index(py_end_token)
    js_context = execjs.compile(js_calc[py_start:py_end])

    interest = js_context.call(
        'recalculate_interest',
        price,
        first_payment,
        credit_length,
        no_insurance,
        no_confirmation,
        variation
    )

    credit = js_context.call(
        'calculate_credit',
        price,
        first_payment,
        credit_length,
        interest
    )

    return int(float(credit['total']) / (credit_length * 30))


def calculate_best_interest_and_credit(price):
    return calculate_interest_and_credit(price, 0.59*price, 60, False, False, 'best')
