"use strict";

function populate_select(select, list) {
    select
        .children()
        .remove()
        .end()
    $.each(list, function(i, item, arr) {
        select
            .append($("<option></option>")
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

//function show_modifications(new_url){
//    window.location.href = new_url;
//};
//
//function show_model_families(mark){
//    window.location.href = "/c/" + mark;
//};

//function get_models(){
//    if ($("#select-marks").val() === ""){
//        clear_select($("#select-models"));
//        clear_select($("#select-modifications"));
//    } else {
//        $.ajax({
//            url: "/ajax/car-models/",
//            type: "GET",
//            data: {
//                mark: $("#select-marks").val()
//            },
//            dataType: "json",
//            success: function(json){
//                populate_select($("#select-models"), json.result);
//                clear_select($("#select-modifications"));
//            }
//        });
//    }
//}
//
//function get_modifications(){
//    $.ajax({
//        url: "/ajax/modifications/",
//        type: "GET",
//        data: {
//            mark: $("#select-marks").val(),
//            car_model: $("#select-models").val()
//        },
//        dataType: "json",
//        success: function(json){
//            populate_select($("#select-modifications"), json.result);
//        }
//    });
//}
//
//$(function(){
//    $("#select-marks").val("");
//});

$(document).ready(function(){
//    $("#select-marks").change(get_models);
//    $("#select-models").change(get_modifications);

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
        }
    });


    // контроллирует сворачиваемость на странице модификаций
    $('.collapse').on('show.bs.collapse', function (e) {
        $('.collapse').not(e.target).removeClass('in');
    });
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        $('.tab-pane').not(e.target).removeClass('active');
    });
    $('.my-tabs a').click(function (e) {
        var tab = $(this);

        var dataUl = tab.parents('ul');

        var setData = function (data) {
            // TODO есть ситуации, в которых не все разделы заполнены. они будут "некликабельны"
            // alert(data['equipment']);
            for (var equipmentGroup in data['equipment']) {
                var equipmentList = $('#' + equipmentGroup + data['mod_id']);
                for (var equipment in data['equipment'][equipmentGroup]) {
                    var cost;
                    if (data['equipment'][equipmentGroup][equipment] != 0) {
                        cost = ' (' + data['equipment'][equipmentGroup][equipment] + ' ₽)';
                    } else {
                        cost = '';
                    }

                    equipmentList.append(
                        '<li class="list-group-item">'
                        + equipment
                        + cost
                        + '</li>'
                    )
                }
            }

            // alert(data['features']);
            for (var featureGroup in data['features']) {
                var featuresList = $('#' + featureGroup + data['mod_id']);
                for (var feature in data['features'][featureGroup]) {
                    featuresList.append(
                        '<li class="list-group-item">'
                        + feature
                        + ': '
                        + data['features'][featureGroup][feature]
                        + '</li>'
                    )
                }
            }
        };

        if (!dataUl.hasClass('loaded')) {
            var modId = dataUl.attr('data-mod-id');
            $.getJSON('/api/modification/' + modId + '/data')
                .done(setData);
            dataUl.addClass('loaded');
        }
        if(tab.parents('li').hasClass('active')){
            window.setTimeout(function(){
                $(".tab-pane").removeClass('active');
                tab.parents('li').removeClass('active');
            },1);
        }
    });

    // схлопываем блок с популярными моделями на мобильных
    $('.btn-popular-models').on('click', function(){
        $('#popular-models').toggleClass('hidden-xs');
    });

    // до сих

//    $("#show-all-marks").click(function(){
//        $("#all-marks").removeClass("hidden");
//        $("#show-all-marks").addClass("hidden");
//    });
});