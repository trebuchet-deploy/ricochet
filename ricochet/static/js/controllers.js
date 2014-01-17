'use strict';

var ricochetApp = angular.module('ricochetApp', []);

ricochetApp.factory('ricochetService', function($http) {
   return {
        getRepoList: function() {
            return $http.get('/repolist')
                .then(function(result) {
                    return result.data;
                });
        },
        getRepo: function(repoName) {
            var url = '/repo/' + repoName;
            return $http.get(url)
                .success(function(result) {
                    return result.data;
                });
        }
   }
});

ricochetApp.controller('RicochetCtrl', function ($scope, $log, $http) {
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
        if (repo.active) {
            $scope.repos[repo.name].active = '';
        } else {
            $http.get('/repo/' + repo.name, {})
                .success(function(data) {
                    $log.error(data);
                    $scope.repos[repo.name].name = repo.name;
                    $scope.repos[repo.name].minion_data = data.minion_data;
                    $scope.repos[repo.name].deploy_data = data.deploy_data;
                    $scope.repos[repo.name].lock_data = data.lock_data;
                    $scope.repos[repo.name].active = 'active';
                });
        }
    }

    $scope.refreshRepo = function(repo) {
        $http.get('/repo/' + repo.name, {})
            .success(function(data) {
                $log.error(data);
                $scope.repos[repo.name].name = repo.name;
                $scope.repos[repo.name].minion_data = data.minion_data;
                $scope.repos[repo.name].deploy_data = data.deploy_data;
                $scope.repos[repo.name].lock_data = data.lock_data;
                $scope.repos[repo.name].active = 'active';
            });
    }
    $scope.debugLog = function(data) {
        $log.error(data);
    }
});
