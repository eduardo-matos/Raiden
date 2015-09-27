describe('Raiden services', function() {
    var $httpBackend, TasksService;

    beforeEach(module('raiden'))
    beforeEach(inject(function(_$httpBackend_, _TasksService_) {
        $httpBackend = _$httpBackend_;
        TasksService = _TasksService_;
    }));

    describe('Tasks', function () {

        it('should return all posts if request is successful', function () {
            fake_response = {data: {slug: 'ham', title: 'spam', item_count: 10, current_count: 9}, success: true}
            $httpBackend.when('GET', '/api/tasks').respond(200, fake_response);

            $httpBackend.expectGET('/api/tasks');

            TasksService.all().then(function (data) {
                expect(data).toEqual(fake_response.data);
            }, function () {
                fail('Request should be successful');
            });

            $httpBackend.flush();
        });

        it('should return message if request is unsuccessful', function () {
            fake_response = {data: {slug: 'ham', title: 'spam', item_count: 10, current_count: 9}, success: false}
            $httpBackend.when('GET', '/api/tasks').respond(200, fake_response);

            $httpBackend.expectGET('/api/tasks');

            TasksService.all().then(function () {
                fail('Request should not be successful');
            }, function (data) {
                expect(data).toEqual({msg: 'Problem loading tasks.'});
            });

            $httpBackend.flush();
        });

        it('should return message if response status is not 200, regardless of success attribute', function () {
            fake_response = {data: {slug: 'ham', title: 'spam', item_count: 10, current_count: 9}, success: true}
            $httpBackend.when('GET', '/api/tasks').respond(400, fake_response);

            $httpBackend.expectGET('/api/tasks');

            TasksService.all().then(function () {
                fail('Request should not be successful');
            }, function (data) {
                expect(data).toEqual({msg: 'Could not access endpoint.'});
            });

            $httpBackend.flush();
        });

    });

    describe('SocketIO', function () {
        // Wish I could test it =(
    });
});
