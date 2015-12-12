/**
* CreditCalc controller
* @namespace kreddb.controllers
*/
(function () {
    'use strict'

    angular
        .module('kreddb.controllers')
        .controller('CreditCalcController', CreditCalcController)

    CreditCalcController.$inject = []
    /**
    * @namespace CreditCalcController
    */
    function CreditCalcController() {
        var INTEREST_RATE = {
            'less_5': { 'from_10': 22, 'from_20': 21, 'from_30': 20, 'from_40': 18, 'from_50': 16 },
            'less_4': { 'from_10': 22, 'from_20': 21, 'from_30': 20, 'from_40': 16, 'from_50': 15 },
            'less_3': { 'from_10': 21, 'from_20': 20, 'from_30': 18, 'from_40': 15, 'from_50': 12 },
            'less_2': { 'from_10': 20, 'from_20': 18, 'from_30': 15, 'from_40': 13, 'from_50': 10 },
            'less_1': { 'from_10': 18, 'from_20': 16, 'from_30': 14, 'from_40': 12, 'from_50': 9 }
        }

        var AMOUNT_MODIFIER = [[1000000, 1], [1500000, 1.1], [2500000, 1.2], [Infinity, 1.3]]
        
        var VARIATON = {
            'real': 1,
            'better': 0.8,
            'best': 0.6 
        }

        var vm = this

        // Влияют на ставку
        vm.first_payment = 10
        vm.credit_length = 12
        vm.no_insurance = false
        vm.no_confirmation = false
        vm.variation = 'real'

        // Участвуют в расчёте
        vm.price = null
        vm.percent = null
        
        vm.credit = []

        vm.recalculate_interest = recalculate_interest
        vm.calculate_credit = calculate_credit

        function recalculate_interest() {
            var key1 = 'less_' + String(Math.floor(vm.credit_length / 12)),
                key2 = 'from_' + String(Math.floor(vm.first_payment / 10) * 10),
                amount = vm.price * (1 - vm.first_payment / 100),
                rate_value = INTEREST_RATE[key1][key2]

            for (var i = 0; i < AMOUNT_MODIFIER.length; i++) {
                var limit = AMOUNT_MODIFIER[i]
                if (amount < limit[0]) {
                    rate_value *= limit[1]
                    break
                }
            }

            if (vm.no_insurance) {
                rate_value *= 1.1
            }

            if (vm.no_confirmation) {
                rate_value *= 1.1
            }

            // TODO: переделать на свитч
            rate_value *= VARIATON[vm.variation]

            vm.percent = parseFloat(rate_value.toFixed(2))
            
            vm.calculate_credit()
        }

        function calculate_credit() {
            var debt = vm.price * (1 - vm.first_payment / 100),
                interest_rate = vm.percent / 100,
                monthly = debt * (interest_rate + interest_rate / (Math.pow((1 + interest_rate / 12), vm.credit_length) - 1)) / 12,
                credit = []

            var num = 0
            while (debt > 1) {
                var monthly_interest = interest_rate / 12 * debt,
                    installment = monthly - monthly_interest,
                    this_month = {
                        'num': ++num,
                        'debt': debt.toFixed(2),
                        'interest': (interest_rate * debt / 12).toFixed(2),
                        'installment': installment.toFixed(2)
                    }
                credit.push(this_month)
                debt -= installment
            }
            vm.credit = credit
        }

    }
})()