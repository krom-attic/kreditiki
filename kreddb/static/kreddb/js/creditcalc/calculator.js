var calculator = (function () {

    // py_start
    var INTEREST_RATE = {
        'less_5': {'from_10': 23, 'from_20': 22, 'from_30': 21, 'from_40': 19, 'from_50': 17},
        'less_4': {'from_10': 23, 'from_20': 22, 'from_30': 21, 'from_40': 17, 'from_50': 16},
        'less_3': {'from_10': 22, 'from_20': 21, 'from_30': 19, 'from_40': 16, 'from_50': 13},
        'less_2': {'from_10': 21, 'from_20': 19, 'from_30': 16, 'from_40': 14, 'from_50': 11},
        'less_1': {'from_10': 19, 'from_20': 17, 'from_30': 15, 'from_40': 13, 'from_50': 10}
    };

    var AMOUNT_MODIFIER = [[1000000, 1], [1500000, 1.1], [2500000, 1.2], [Infinity, 1.3]];

    var VARIATION = {
        'real': 1,
        'better': 0.8,
        'best': 0.6
    };

    var recalculate_interest = function (price, first_payment, credit_length, no_insurance, no_confirmation, variation) {

        var key1 = 'less_' + String(Math.floor((credit_length - 1) / 12) + 1),
            key2 = 'from_' + String(Math.floor(10 * first_payment / price) * 10),
            amount = price - first_payment,
            rate_value = INTEREST_RATE[key1][key2];

        for (var i = 0; i < AMOUNT_MODIFIER.length; i++) {
            var limit = AMOUNT_MODIFIER[i];
            if (amount < limit[0]) {
                rate_value *= limit[1];
                break
            }
        }

        if (no_insurance) {
            rate_value *= 1.1
        }

        if (no_confirmation) {
            rate_value *= 1.1
        }

        // TODO: переделать на свитч
        rate_value *= VARIATION[variation];

        return parseFloat(rate_value.toFixed(2));

    };

    var calculate_credit = function (price, first_payment, credit_length, percent) {
        var debt = price - first_payment,
            interest_rate = percent / 100,
            monthly = debt * (interest_rate + interest_rate / (Math.pow((1 + interest_rate / 12), credit_length) - 1)) / 12,
            credit = [];

        var num = 0;
        var total = first_payment;
        while (debt > 1) {
            var monthly_interest = interest_rate / 12 * debt,
                installment = monthly - monthly_interest,
                interest = (interest_rate * debt / 12),
                this_month = {
                    'num': ++num,
                    'debt': debt.toFixed(2),
                    'interest': interest.toFixed(2),
                    'installment': installment.toFixed(2)
                };
            total += (interest + installment);
            credit.push(this_month);
            debt -= installment
        }
        return {
            'credit': credit,
            'total': total.toFixed(2)
        };
    };
    // py_end

    return {
        recalculate_interest: recalculate_interest,
        calculate_credit: calculate_credit
    }
})();