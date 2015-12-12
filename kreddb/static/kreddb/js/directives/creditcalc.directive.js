/**
* CreditCalc
* @namespace kreddb.directives
*/
(function () {
  'use strict';

  angular
    .module('kreddb.directives')
    .directive('creditcalc', creditcalc);


  /**
  * @namespace CreditCalc
  */
  function creditcalc() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf kreddb.directives.CreditCalc
    */

    var directive = {
      controller: 'CreditCalcController',
      controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/kreddb/templates/creditcalc.html'
    };

    return directive;
  }
})();