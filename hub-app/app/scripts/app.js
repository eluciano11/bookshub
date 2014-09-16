'use strict';

/**
 * @ngdoc overview
 * @name hubAppApp
 * @description
 * # hubAppApp
 *
 * Main module of the application.
 */
angular
  .module('hubAppApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });


























(function(){

  var app = angular.module('signUp',[]);

  app.controller('BookSUController',function(){

     







  });

});


















  