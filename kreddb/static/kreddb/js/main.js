"use strict";

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