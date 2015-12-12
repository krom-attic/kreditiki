/**
* Modifications
* @namespace kreddb.services
*/
(function () {
  'use strict';

  angular
    .module('kreddb.services')
    .factory('Modifications', Modifications);

  Modifications.$inject = ['$http'];

  /**
  * @namespace Modifications
  * @returns {Factory}
  */
  function Modifications($http) {
    /**
    * @name Modifications
    * @desc The Factory to be returned
    */
    var Modifications = {
      get_modifications: get_modifications
    };

    return Modifications;

    ////////////////////

    /**
    * @name get_modifications
    * @desc Gets car modifications for the model and the make
    * @param {string} carmake The make of a car
    * @param {string} carmodel The model of a car
    * @returns {Promise}
    * @memberOf kreddb.services.Modifications
    */
    function get_modifications(carmake, carmodel) {
      return $http.get('/api/v1/modifications/' + carmake + '/' + carmodel + '/');
    }
  }
})();