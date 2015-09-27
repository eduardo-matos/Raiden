describe('Raiden services', function() {
    var $httpBackend, $controller, $rootScope, TasksService;

    beforeEach(module('raiden'))
    beforeEach(inject(function(_$httpBackend_, _$controller_, _$rootScope_, _TasksService_) {
        $httpBackend = _$httpBackend_;
        $controller = _$controller_;
        $rootScope = _$rootScope_;
        TasksService = _TasksService_;
    }));

    describe('Tasks Controller  Startup', function () {
        var controller;

        it('should populate scope with tasks', function () {
            fake_response = {data: [{slug: 'ham', title: 'spam', item_count: 10, current_count: 9}], success: true}
            $httpBackend.when('GET', '/api/tasks').respond(200, fake_response);

            var scope = $rootScope.$new();
            controller = $controller('TasksCtrl', {
                $scope: scope,
                SocketIO: {on: function() {}}
            });
            $httpBackend.flush();

            expect(scope.tasks).toEqual({'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 9, percent: 90}});
        });

    });

    describe('Tasks Controller SocketIO', function () {
        var controller, scope, callback_new_task, callback_progress_task;

        beforeEach(function () {
            scope = $rootScope.$new();
            controller = $controller('TasksCtrl', {
                $scope: scope,
                SocketIO: {on: function(evt, func) {
                    if(evt == 'new_task') {
                        callback_new_task = func;
                    } else if(evt == 'progress_task') {
                        callback_progress_task = func;
                    }
                }}
            });
        });

        it("should add new task on 'new_task' event", function () {
            spyOn(scope, '$digest')
            callback_new_task({slug: 'spam', title: 'ham', current_count: 5, item_count: 20});

            expect(scope.tasks).toEqual({'spam': {slug: 'spam', title: 'ham', item_count: 20, current_count: 5, percent: 25}});
        });

        it("should add new task on 'new_task' event", function () {
            scope.tasks = {'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 2, percent: 20}}

            spyOn(scope, '$digest')
            callback_progress_task({slug: 'ham', current_count: 5});

            expect(scope.tasks).toEqual({'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 5, percent: 50}});
        });
    });

    describe('Tasks Controller Helper Functions', function () {
        var controller;

        it('should update existing task', function () {
            var scope = $rootScope.$new();
            controller = $controller('TasksCtrl', {
                $scope: scope,
                SocketIO: {on: function() {}}
            });
            scope.tasks = {'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 2, percent: 90}}

            scope.progress_task('ham', 5);
            expect(scope.tasks).toEqual({'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 5, percent: 50}});
        });

        it('should do nothing if slug doesnt exist', function () {
            var scope = $rootScope.$new();
            controller = $controller('TasksCtrl', {
                $scope: scope,
                SocketIO: {on: function() {}}
            });

            scope.progress_task('ham', 5);
            expect(scope.tasks).toEqual({});
        });

        it('should add new task', function () {
            var scope = $rootScope.$new();
            controller = $controller('TasksCtrl', {
                $scope: scope,
                SocketIO: {on: function() {}}
            });

            scope.new_task('ham', 'spam', 10, 2);
            expect(scope.tasks).toEqual({'ham': {slug: 'ham', title: 'spam', item_count: 10, current_count: 2, percent: 20}});
        });

    });

});
