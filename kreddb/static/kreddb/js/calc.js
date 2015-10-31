"use strict";

function calculate(loan, length, interest_p) {
    var credit = [],
        interest_p = interest_p / 100,
        monthly = loan * (interest_p + interest_p / (Math.pow((1+interest_p/12), length) - 1)) / 12,
        debt = loan;

    while (debt > 1) {
        var interest_m = interest_p / 12 * debt,
            installment = monthly - interest_m,
            this_month = {
            'debt': debt.toFixed(2),
            'interest': (interest_p*debt/12).toFixed(2),
            'installment': installment.toFixed(2)
            }
        credit.push(this_month);
        debt -= installment
    }
    return credit
};

var INTEREST_RATE = {
    'less_5': {'from_10': 22, 'from_20': 21, 'from_30': 20, 'from_40': 18, 'from_50': 16},
    'less_4': {'from_10': 22, 'from_20': 21, 'from_30': 20, 'from_40': 16, 'from_50': 15},
    'less_3': {'from_10': 21, 'from_20': 20, 'from_30': 18, 'from_40': 15, 'from_50': 12},
    'less_2': {'from_10': 20, 'from_20': 18, 'from_30': 15, 'from_40': 13, 'from_50': 10},
    'less_1': {'from_10': 18, 'from_20': 16, 'from_30': 14, 'from_40': 12, 'from_50': 9}
};

var AMOUNT_MODIFIER = [[1000000, 1], [1500000, 1.1], [2500000, 1.2], [Infinity, 1.3]];

function recalculate_interest() {
    var price = parseInt($("#price").val()),
        first_payment = parseInt($("#first_payment").val()),
        credit_length = parseInt($("#months").val()),
        no_insurance = $("#no_insurance").prop("checked"),
        no_confirmation = $("#no_confirmation").prop("checked"),
        variation_better = $("#variation_better").prop("checked"),
        variation_best = $("#variation_best").prop("checked");

    var key1 = 'less_' + String(Math.floor(credit_length / 12)),
        key2 = 'from_' + String(Math.floor(first_payment / 10) * 10),
        amount = price*(1-first_payment/100),
        rate_value = INTEREST_RATE[key1][key2]

    for (var i = 0; i < AMOUNT_MODIFIER.length; i++) {
        var limit = AMOUNT_MODIFIER[i];
        if (amount < limit[0]) {
            rate_value *= limit[1];
            break;
        };
    };

    if (no_insurance) {
        rate_value *= 1.1;
    }

    if (no_confirmation) {
        rate_value *= 1.1;
    }

    if (variation_better) {
        rate_value *= .8;
    };

    if (variation_best) {
        rate_value *= .6;
    };

    $("#percent").val((rate_value).toFixed(2))
};


$(document).ready(function(){
    $("#calculate").click(function(){
        var price = parseInt($("#price").val()),
            first_payment = parseInt($("#first_payment").val()),
            credit_length = parseInt($("#months").val()),
            interest_p = parseInt($("#percent").val()),
            credit = calculate(price*(1-first_payment/100), credit_length, interest_p);

        var result_table = "<table style='width:30%'><thead><tr><th>Месяц</th><th>Долг</th><th>Проценты</th><th>Тело</th></tr></thead>"
        for (var i = 0; i < credit.length; i++) {
            result_table += ("<tr>");
            result_table += ("<td>" + (i+1) + "</td>");
            result_table += ("<td>" + credit[i].debt + "</td>");
            result_table += ("<td>" + credit[i].interest + "</td>");
            result_table += ("<td>" + credit[i].installment + "</td>");
            result_table += ("</tr>");
        }
        result_table += ("</table>");
        $("#result").html(result_table);
    });

    $("#months").change(function(){
        recalculate_interest();
    });

    $("#first_payment").change(function(){
        recalculate_interest();
    });

    $("#price").change(function(){
        recalculate_interest();
    });

    $("#no_insurance").change(function(){
        recalculate_interest();
    });

    $("#no_confirmation").change(function(){
        recalculate_interest();
    });

    $('input[name="variation"]').change(function(){
        recalculate_interest();
    });

});