;(function () {
    'use strict'

    angular
        .module('kreddb.services')
        .filter('round', Round)

    function Round() {
        return function (input) {
            return Math.round(input)
        }
    }

})()