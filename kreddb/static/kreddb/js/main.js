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

function populate_select(select, list) {
    select
        .children()
        .remove()
        .end()
    $.each(list, function(i, item, arr) {
        select
            .append($("<option></option")
            .attr("value", item)
            .text(item));
    });
};

function clear_select(select) {
    select
        .children()
        .remove()
        .end()
};

function show_modifications(new_url){
    window.location.href = new_url;
};

function show_car_models(mark){
    window.location.href = "/c/" + mark;
};

function get_models(){
    if ($("#select-marks").val() === ""){
        clear_select($("#select-models"));
        clear_select($("#select-modifications"));
    } else {
        $.ajax({
            url: "/ajax/car-models/",
            type: "GET",
            data: {
                mark: $("#select-marks").val()
            },
            dataType: "json",
            success: function(json){
                populate_select($("#select-models"), json.result);
                clear_select($("#select-modifications"));
            }
        });
    }
}

function get_modifications(){
    $.ajax({
        url: "/ajax/modifications/",
        type: "GET",
        data: {
            mark: $("#select-marks").val(),
            car_model: $("#select-models").val()
        },
        dataType: "json",
        success: function(json){
            populate_select($("#select-modifications"), json.result);
        }
    });
}

$(function(){
    $("#select-marks").val("");
});

$(document).ready(function(){
    $("#calculate").click(function(){
        var loan = parseInt($("#loan").val()),
            credit_length = parseInt($("#months").val()),
            interest_p = parseInt($("#percent").val()),
            credit = calculate(loan, credit_length, interest_p);

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
    $("#select-marks").change(get_models);
    $("#select-models").change(get_modifications);

    $("#search-btn").click(function(){
        if (!($("#select-marks").val() === "" || $("#select-models").val() === "")){
            $.ajax({
                url: "/ajax/modification-search/",
                type: "GET",
                data: {
                    mark: $("#select-marks").val(),
                    car_model: $("#select-models").val(),
                    modification: $("#select-modifications").val()
                },
                dataType: "json",
                success: function(json){
                    show_modifications(json.result);
                }
            });
        } else if (!($("#select-marks").val() === "")){
            show_car_models($("#select-marks").val());
        };
    });

//    $("#show-all-marks").click(function(){
//        $("#all-marks").removeClass("hidden");
//        $("#show-all-marks").addClass("hidden");
//    });
});