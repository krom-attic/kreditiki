/**
* CarSelector
* @namespace kreddb.directives
*/
(function () {
  'use strict';

  angular
    .module('kreddb.directives')
    .directive('carselector', carselector);


  /**
  * @namespace CarSelector
  */
  function carselector() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf kreddb.directives.CarSelector
    */

    var directive = {
      controller: 'CarSelectorController',
      controllerAs: 'vm',
      restrict: 'E',
//      scope: {
//        carmake: '=',
//      },
      templateUrl: '/static/kreddb/templates/carselector.html'
    };

    return directive;
  }
})();