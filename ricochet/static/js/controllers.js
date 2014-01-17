'use strict';

var ricochetApp = angular.module('ricochetApp', []);

ricochetApp.controller('RicochetCtrl', function ($scope, $timeout, $log, $http) {
    $scope.repos = {};
    var repoListCallback = function(repoList) {
        var repos = new Object();

        for (var i = 0; i < repoList.length; i++) {
            var repo = new Object;
            repo.name = repoList[i];
            repos[repo.name] = repo;
        }
        $scope.repos = repos;
    }
    $http.get('/repolist').success(repoListCallback);

    $scope.toggleRepo = function(repo) {
        var timer;
        if (repo.active) {
            clearInterval($scope.repos[repo.name].timer);
            $scope.repos[repo.name].active = '';
            $scope.repos[repo.name].paused = true;
        } else {
            // Gross. Fix this code duplication with a factory.
            $http.get('/repo/' + repo.name, {})
                .success(function(data) {
                    $log.error(data);
                    $scope.repos[repo.name].name = repo.name;
                    $scope.repos[repo.name].minion_data = data.minion_data;
                    $scope.repos[repo.name].deploy_data = data.deploy_data;
                    $scope.repos[repo.name].lock_data = data.lock_data;
                    $scope.repos[repo.name].active = 'active';
                    $scope.repos[repo.name].paused = true;
                });
            $scope.repos[repo.name].func = function() {
                    $http.get('/repo/' + repo.name, {})
                        .success(function(data) {
                            $log.error(data);
                            $scope.repos[repo.name].name = repo.name;
                            $scope.repos[repo.name].minion_data = data.minion_data;
                            $scope.repos[repo.name].deploy_data = data.deploy_data;
                            $scope.repos[repo.name].lock_data = data.lock_data;
                            $scope.repos[repo.name].active = 'active';
                            $scope.repos[repo.name].paused = true;
                        });
                };
            $scope.repos[repo.name].timer = setInterval($scope.repos[repo.name].func, 2000);
            $scope.repos[repo.name].paused = false;
        }
    }

    $scope.toggleRefresh = function(repo) {
        if ($scope.repos[repo.name].paused) {
            clearInterval($scope.repos[repo.name].timer);
            $scope.repos[repo.name].paused = false;
        } else {
            clearInterval($scope.repos[repo.name].timer);
            $scope.repos[repo.name].timer = setInterval($scope.repos[repo.name].func, 2000);
            $scope.repos[repo.name].paused = true;
        }
    }
    $scope.debugLog = function(data) {
        $log.error(data);
    }
});
