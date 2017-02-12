/**
* CreditCalc controller
* @namespace kreddb.controllers
*/
;(function () {
    'use strict';

    angular
        .module('kreddb.controllers')
        .controller('CreditCalcController', CreditCalcController);

    CreditCalcController.$inject = ['$http'];
    /**
    * @namespace CreditCalcController
    */
    function CreditCalcController($http) {

        var INITIAL_PAYMENT = 0.1;

        var vm = this;

        vm.photos = null;
        vm.car_name = null;
        vm.modifications = null;

        // Участвуют в расчёте
        vm.modification = {"price": 0};
        vm.percent = null;

        // Влияют на ставку
        vm.first_payment = null;
        vm.credit_length = 12;
        vm.no_insurance = false;
        vm.no_confirmation = false;
        vm.variation = 'better';

        vm.credit = [];
        vm.total_credit = null;

        vm.recalculate_interest = function () {
            vm.percent = calculator.recalculate_interest(
                vm.modification.price,
                parseInt(vm.first_payment, 10),
                parseInt(vm.credit_length, 10),
                vm.no_insurance,
                vm.no_confirmation,
                vm.variation
            );
            vm.calculate_credit()
        };

        vm.calculate_credit = function () {
            var credit_calculation = calculator.calculate_credit(
                vm.modification.price,
                parseInt(vm.first_payment, 10),
                parseInt(vm.credit_length, 10),
                vm.percent
            );
            vm.credit = credit_calculation['credit'];
            vm.total_credit = credit_calculation['total'];
        };

        vm.selectModification = function () {
            vm.payment_min = Math.ceil(INITIAL_PAYMENT * vm.modification.price / 1000) * 1000;
            vm.payment_max = Math.floor(0.59 * vm.modification.price / 1000) * 1000;
            vm.first_payment = vm.payment_min;
            vm.recalculate_interest();
            vm.calculate_credit()
        };

        vm.init = function (app_context) {
        // TODO нужно разварачивать словарь app_context прямо в vm
            vm.photos = app_context["photos"];
            vm.car_name = app_context["car_name"];
            vm.modifications = app_context["modifications"];
            vm.modification = vm.modifications[0];
            vm.selectModification();
        };

        vm.application = {

        };

        vm.submit = function () {
            vm.application["url"] = window.location.href;
            vm.application["first_payment"] = vm.first_payment;
            vm.application["credit_length"] = vm.credit_length;
            vm.application["no_insurance"] = vm.no_insurance;
            vm.application["no_confirmation"] = vm.no_confirmation;
            vm.application["variation"] = vm.variation;
            $http({
                method: "POST",
                url: "/заявка/",
                data: vm.application
            })
                .success(function () {
                    alert('Спасибо за заявку!\nНаш менеджер свяжется с Вами в ближайшее время.')
                })
        }
    }
})();