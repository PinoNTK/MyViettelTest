angular.module('myApp', ['angularUtils.directives.dirPagination'])
            .controller('HomeCtrl', function($scope, $http) {
    //         	$scope.pageInfo={}
				// // Paging sever-side
    //         	var vm = this;
			 //    vm.accounts = []; //declare an empty array
			 //    vm.pageno = 1; // initialize page no to 1
			 //    vm.total_count = 0;
			 //    vm.itemsPerPage = 10; //this could be a dynamic value from a drop down
			 //    $scope.pageInfo.itemsPerPage = itemsPerPage
			 //    $scope.pageInfo.pagenumber= pagenumber
			 //    vm.getData = function(pageno){ // This would fetch the data on page change.
			 //        //In practice this should be in a factory.
			 //        $http({
				// 		method: 'POST',
				// 		url: '/getAccountPage',
				// 		data: {pageInfo:$scope.pageInfo}
				// 	}).then(function(response) {
				// 		vm.accounts = response.data;  // data to be displayed on current page.
			 //            // vm.total_count = response.data.total_count; // total data count.
				// 		console.log('mm',accounts);
				// 	}, function(error) {
				// 		console.log(error);
				// 	});
			 //    };
    // 			vm.getData(vm.pageno); // Call the function to fetch initial data on page load.


				$scope.info = {};
				$scope.searchData = {};
				$scope.searchBirthData = {};
				
				$scope.showAdd = true;
				$scope.sort = function(keyname){
        			$scope.sortKey = keyname;   //set the sortKey to the param passed
        			$scope.reverse = !$scope.reverse; //if true make it false and vice versa
    			}
			
				$scope.showlist = function(){
					$http({
						method: 'POST',
						url: '/getAccountList',

					}).then(function(response) {
						accounts=$scope.accounts = response.data;

						
						// console.log('mm',accounts);
					}, function(error) {
						console.log(error);
					});
				}
                
				
				$scope.addAccount = function(){
					
					$scope.info.gender=$('select[name=selectedGender]').val();
					$scope.info.memberSince=$('#txtMemberSince').val().toString();
					$scope.info.birthday=$('#txtBirthDay').val().toString();
					// console.log($scope.info.gender,$scope.info.memberSince,$scope.info.birthday,$scope.info.name,$scope.info.cardNumber,$scope.info.username,$scope.info.password,$scope.info.accountBalance,$scope.info.role,$scope.info.accountNumber,$scope.info.address)
					$http({
						method: 'POST',
						url: '/addAccount',
						data: {info:$scope.info}
					}).then(function(response) {
						$scope.showlist();
						$('#addPopUp').modal('hide')
						$scope.info = {}
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.editAccount = function(accountId){
					$scope.info.accountId = accountId;
					
					$scope.showAdd = false;

					$http({
						method: 'POST',
						url: '/getAccount',
						data: {accountId:$scope.info.accountId}
					}).then(function(response) {
						// console.log(response);
						$scope.info = response.data;
						$('#addPopUp').modal('show')
						if($scope.info!=null && $scope.info!=undefined){
							var gender = $scope.info.gender;
							if(gender.toLowerCase()=='male'){
						 		$('#male').prop("selected","selected");
						 	}
						 	else if(gender.toLowerCase()=='female'){
						 		$('#female').prop("selected","selected");
						 	}
						 	else{
						 		$('#unidentified').prop("selected","selected");
						 	}
						// console.log(gender)
						}
						
					}, function(error) {
						console.log(error);
					});

				}
				
				$scope.adminSearch = function(){
				
					$scope.searchData.field=$('#searchField').val().trim().toString()
					$scope.searchData.fieldValue=$('#fieldValue').val().trim().toString()
					$http({
						method: 'POST',
						url: '/adminsearch',
						data: {searchData:$scope.searchData}
					}).then(function(response) {
						$scope.accounts = response.data;
						
					}, function(error) {
						console.log(error);
					});
				}
				$scope.adminSearchBirth = function(){
					$scope.searchBirthData.fieldValue=$('#txtsearchBirthDay').val().trim().toString()
					console.log($scope.searchBirthData)
					$http({
						method: 'POST',
						url: '/adminsearchbirth',
						data: {searchBirthData:$scope.searchBirthData}
					}).then(function(response) {
						$scope.accounts = response.data;
						console.log($scope.accounts)
					}, function(error) {
						console.log(error);
					});
				}

				$scope.normalSearch = function(){
				
					$scope.searchData.field=$('#searchField').val().trim().toString()
					$scope.searchData.fieldValue=$('#fieldValue').val().trim().toString()
					$http({
						method: 'POST',
						url: '/normalsearch',
						data: {searchData:$scope.searchData}
					}).then(function(response) {
						$scope.accounts = response.data;
						// console.log(response.data)
					}, function(error) {
						console.log(error);
					});
				}
				
				$scope.updateAccount= function(accountId){
				
					$scope.info.gender=$('select[name=selectedGender]').val()
					$scope.info.birthday=$('#txtBirthDay').val().toString()
					$scope.info.memberSince=$('#txtMemberSince').val().toString()
					$http({
						method: 'POST',
						url: '/updateAccount',
						data: {info:$scope.info}
					}).then(function(response) {
						// console.log(response.data);

						$scope.showlist();
						$('#addPopUp').modal('hide')
					}, function(error) {
						console.log(error);
					});
				}
		
				$scope.showAddPopUp = function(){
					$scope.showAdd = true;
					$scope.info = {};
					$('#addPopUp').modal('show')
				}
				
				$scope.showRunPopUp = function(accountId){
				
					$scope.info.accountId = accountId;
					$scope.run = {};	
					
					$http({
						method: 'POST',
						url: '/getAccount',
						data: {accountId:$scope.info.accountId}
					}).then(function(response) {
						// console.log(response);
						$scope.run = response.data;
						$scope.run.isRoot = false;
						$('#runPopUp').modal('show');
					}, function(error) {
						console.log(error);
					});
				
					
					
				}
				
				$scope.confirmDelete = function(accountId){
					$scope.deleteAccountId = accountId;
					$('#deleteConfirm').modal('show');
				}
				
				$scope.deleteAccount = function(){
					
					$http({
						method: 'POST',
						url: '/deleteAccount',
						data: {accountId:$scope.deleteAccountId}
					}).then(function(response) {
						// console.log(response.data);
						$scope.deleteAccountId = '';
						$scope.showlist();
						$('#deleteConfirm').modal('hide')
					}, function(error) {
						console.log(error);
					});
				}
				
				if($('#auth').text()!='Normal Manager')
					$scope.showlist();
            })