;(function () {
    'use strict';

    angular
        .module('raiden')
        .controller('TasksCtrl', TasksCtrl);

    TasksCtrl.$inject = ['$scope', 'TasksService', 'SocketIO'];
    function TasksCtrl ($scope, TasksService, SocketIO) {
        $scope.tasks = {};
        $scope.new_task = new_task;
        $scope.progress_task = progress_task;

        TasksService.all().then(function (tasks) {
            angular.forEach(tasks, function (task) {
                $scope.new_task(task.slug, task.title, task.item_count, task.current_count);
            });
        });

        SocketIO.on('new_task', function (data) {
            $scope.new_task(data.slug, data.title, data.item_count, data.current_count);
            $scope.$digest();
        });

        SocketIO.on('progress_task', function (data) {
            $scope.progress_task(data.slug, data.current_count);
            $scope.$digest();
        });

        function progress_task(slug, current_count) {
            if(!$scope.tasks[slug]) {
                return;
            }

            $scope.tasks[slug].current_count = current_count;
            $scope.tasks[slug].percent = 100 * current_count / $scope.tasks[slug].item_count;
        }

        function new_task(slug, title, item_count, current_count) {
            var task = {
                slug: slug,
                title: title,
                item_count: item_count,
                current_count: current_count,
                percent: 100 * current_count / item_count
            };

            $scope.tasks[slug] = task;
        }
    }
}());
