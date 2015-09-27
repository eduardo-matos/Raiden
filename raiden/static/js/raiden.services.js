;(function () {
    'use strict';

    angular
        .module('raiden')
        .factory('SocketIO', SocketIO)
        .factory('TasksService', TasksService);

    function SocketIO () {
        var socket = io.connect('http://' + document.domain + ':' + location.port);

        // looks like a bug in Flask-SocketIO.
        // We have to "warm up" the websocket.
        socket.on('connect', function () {
            socket.emit('connect');
        });

        return socket;
    }

    TasksService.$inject = ['$http', '$q'];
    function TasksService ($http, $q) {
        return {
            all: all
        };

        function all () {
            var deferred = $q.defer();

            $http.get('/api/tasks').then(on_success, on_error);

            return deferred.promise;

            function on_success (response) {
                if(response.status == 200 && response.data.success) {
                    deferred.resolve(response.data.data);
                } else {
                    deferred.reject({msg: 'Problem loading tasks.'});
                }
            }

            function on_error (response) {
                deferred.reject({msg: 'Could not access endpoint.'})
            }
        }
    }

}());
