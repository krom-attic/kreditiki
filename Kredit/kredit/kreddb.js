(function () {
    'use strict'

    angular
        .module('kreddb', [
            'kreddb.controllers',
            'kreddb.directives',
            'kreddb.services'
        ])

    angular
        .module('kreddb.controllers', [])

    angular
        .module('kreddb.directives', [])

    angular
        .module('kreddb.services', [])
})()

angular.module('sliderDemo1', ['ngMaterial'])
.controller('AppCtrl', function($scope) {
  $scope.color = {
    red: Math.floor(Math.random() * 255),
    green: Math.floor(Math.random() * 255),
    blue: Math.floor(Math.random() * 255)
  };
  $scope.rating1 = 3;
  $scope.rating2 = 2;
  $scope.rating3 = 4;
  $scope.disabled1 = 0;
  $scope.disabled2 = 70;
});