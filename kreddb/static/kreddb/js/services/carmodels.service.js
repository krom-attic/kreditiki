/**
* CarModels
* @namespace kreddb.services
*/
;(function () {
  'use strict';

  angular
    .module('kreddb.services')
    .factory('CarModels', CarModels);

  CarModels.$inject = ['$http'];

  /**
  * @namespace CarModels
  * @returns {Factory}
  */
  function CarModels($http) {
    /**
    * @name CarModels
    * @desc The Factory to be returned
    */
    var CarModels = {
      get_carmodels: get_carmodels
    };

    return CarModels;

    ////////////////////

    /**
    * @name get_carmodels
    * @desc Gets car models for a make
    * @param {string} make The make of a car
    * @returns {Promise}
    * @memberOf kreddb.services.CarModels
    */
    function get_carmodels(carmake) {
      return $http.get('/api/v1/carmodels/' + carmake +'/');
    }
  }
})();