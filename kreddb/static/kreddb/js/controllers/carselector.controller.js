/**
* CarSelector controller
* @namespace kreddb.controllers
*/
;(function () {
    'use strict'

    angular
        .module('kreddb.controllers')
        .controller('CarSelectorController', CarSelectorController)

    CarSelectorController.$inject = ['CarModels']

    /**
    * @namespace CarSelectorController
    */
    function CarSelectorController(CarModels) {
        var vm = this

        vm.carmake = null
        vm.carmodel = null

        vm.carmodels = []
        vm.get_carmodels = get_carmodels

        /**
        * @name get_carmodels
        * @desc Gets a list of car models for the make
        * @memberOf kreddb.controllers.CarSelectorController
        */
        function get_carmodels() {
            function set_carmodels(carmodels) {
                vm.carmodels = carmodels.data
            }

            CarModels.get_carmodels(vm.carmake)
                .then(set_carmodels, set_carmodels)
        }
    }
})()
