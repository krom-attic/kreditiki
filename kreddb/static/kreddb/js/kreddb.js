;(function () {
    'use strict';

    angular
        .module('kreddb', [
            'kreddb.controllers',
            'kreddb.directives',
            'kreddb.services',
            'kreddb.filters'
        ])
        .config(['$httpProvider', function ($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }]);

    angular
        .module('kreddb.controllers', []);

    angular
        .module('kreddb.directives', []);

    angular
        .module('kreddb.services', []);

    angular
        .module('kreddb.filters', [])
})();