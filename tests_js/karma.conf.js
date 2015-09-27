module.exports = function(config) {
  config.set({
    basePath: '../raiden/static',
    frameworks: ['jasmine'],
    files: [
      'bower_components/angular/angular.js',
      'bower_components/angular-mocks/angular-mocks.js',
      'js/raiden.js',
      'js/raiden.services.js',
      'js/raiden.controllers.js',

      '../../tests_js/spec/**/*.js'
    ],
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['PhantomJS'],
    singleRun: true
  });
};
