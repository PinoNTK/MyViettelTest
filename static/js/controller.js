angular.module('myApp', ['angularUtils.directives.dirPagination'])
.controller('HomeCtrl', function($scope, $http) {
			$scope.pageInfo={}
			$scope.info = {};
			$scope.searchData = {};
			$scope.searchBirthData = {};
			$scope.searchOneBirthData = {};			
			$scope.showAdd = true;


				// Paging sever-side
				// var vm = this;
			 //    vm.accounts = []; //declare an empty array
			 //    vm.pageno = 1; // initialize page no to 1
			 //    vm.total_count = 0;
			 //    vm.itemsPerPage = 10; //this could be a dynamic value from a drop down
			 //    $scope.pageInfo.itemsPerPage = itemsPerPage
			 //    $scope.pageInfo.pagenumber= pagenumber
			 //    vm.getData = function(pageno){ // This would fetch the data on page change.
			 //        //In practice this should be in a factory.
			 //        $http({
			 //        	method: 'POST',
			 //        	url: '/getAccountPage',
			 //        	data: {pageInfo:$scope.pageInfo}
			 //        }).then(function(response) {
				// 		vm.accounts = response.data;  // data to be displayed on current page.
			 //            // vm.total_count = response.data.total_count; // total data count.
			 //            console.log('mm',accounts);
			 //        }, function(error) {
			 //        	console.log(error);
			 //        });
			 //    };
    // 			vm.getData(vm.pageno); // Call the function to fetch initial data on page load.


    			// sort client-side setup
    			$scope.sort = function(keyname){
        			$scope.sortKey = keyname;   //set the sortKey to the param passed
        			$scope.reverse = !$scope.reverse; //if true make it false and vice versa
        		}

        		//API conect
        		$scope.showlist = function(){
        			$http({
        				method: 'POST',
        				url: '/getAccountList',

        			}).then(function(response) {
        				accounts=$scope.accounts = response.data;
        			}, function(error) {
        				console.log(error);
        			});
        		}


        		$scope.addAccount = function(){
        			var sEmail = $('#txtMail').val();
        			var accountBalance = $('#txtAccountBalance').val();
        			var accountNumber = $('#txtAccountNumber').val();
        			var cardNumber = $('#txtCardNumber').val();
        			var phone = $('#txtPhoneNumber').val();
        			var idNumber = $('#txtIDNumber').val();
        			var isnum_accNum = /^\d+$/.test(accountNumber);
        			var isnum_cardNum = /^\d+$/.test(cardNumber);
        			var isnum_accBalance = /^\d+$/.test(accountBalance);
        			var isnum_phoneNum = /^\d+$/.test(phone);
        			var isnum_idNum = /^\d+$/.test(idNumber);
        			console.log(isnum_accNum,isnum_cardNum,isnum_accBalance,isnum_phoneNum,isnum_idNum);
        			if ($.trim(sEmail).length == 0) {
        				alert('Please enter valid email address');
        			}
        			if (!validateEmail(sEmail)||!(isnum_accBalance&&accountBalance>0)||!isnum_cardNum||!isnum_accNum||!isnum_phoneNum||!isnum_idNum) {
        				alert('Please enter valid email address, account balance,card number, account number, ID!');
        				$('#addPopUp').modal('hide');
        			} else{
        				console.log($('#txtName').val());
        				$scope.info.gender=$('select[name=selectedGender]').val().toString().trim();
        				$scope.info.memberSince=$('#txtMemberSince').val().toString().trim();
        				$scope.info.birthday=$('#txtBirthDay').val().toString().trim();
        				$scope.info.name=$('#txtName').val().toString().trim();
        				$scope.info.idNumber=$('#txtIDNumber').val().toString().trim();
        				$scope.info.phone=$('#txtPhoneNumber').val().toString().trim();
        				$scope.info.address=$('#txtAddress').val().toString().trim();
        				$scope.info.mail=$('#txtMail').val().toString().trim();
        				$scope.info.username=$('#txtUsername').val().toString().trim();
        				$scope.info.password=$('#txtPassword').val().toString().trim();
        				$scope.info.accountNumber=$('#txtAccountNumber').val().toString().trim();
        				$scope.info.cardNumber=$('#txtCardNumber').val().toString().trim();
        				$scope.info.accountBalance=$('#txtAccountBalance').val().toString().trim();
        				$scope.info.role=$('#txtRole').val().toString().trim();
					// console.log($scope.info.gender,$scope.info.memberSince,$scope.info.birthday,$scope.info.name,$scope.info.cardNumber,$scope.info.username,$scope.info.password,$scope.info.accountBalance,$scope.info.role,$scope.info.accountNumber,$scope.info.address)
					$http({
						method: 'POST',
						url: '/addAccount',
						data: {info:$scope.info}
					}).then(function(response) {
						$scope.showlist();
						$('#addPopUp').modal('hide')
						$scope.result=response.data;
						console.log($scope.result);
						if($scope.result.status=='OK'){
							$('#resultMessge').modal('show');
							$('#success').text($scope.result.message)
						}
						else{
							$('#resultMessge').modal('show');
							$('#fail').show();
							$('#succeed').hide();
							$('#error').text($scope.result.message)
						}
					}, function(error) {
						console.log(error);
					});
				}

			}
			
			function validateEmail(sEmail) {
				var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
				if (filter.test(sEmail)) {
					return true;
				}
				else {
					return false;
				}
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
			$scope.adminSearchOneBirth = function(){
				$scope.searchOneBirthData.fieldValue=$('#txtsearchBirthDay').val().trim().toString()
				console.log($scope.searchOneBirthData)
				$http({
					method: 'POST',
					url: '/adminsearchonebirth',
					data: {searchOneBirthData:$scope.searchOneBirthData}
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
			$scope.logOut= function(){
				$http({
					method: 'POST',
					url: '/logout',
				}).then(function(response){

				}, function(error){
					console.log(error)
				});
			}

			$scope.updateAccount= function(accountId){

				var sEmail = $('#txtMail').val();
				var accountBalance = $('#txtAccountBalance').val();
				var accountNumber = $('#txtAccountNumber').val();
				var cardNumber = $('#txtCardNumber').val();
				var phone = $('#txtPhoneNumber').val();
				var idNumber = $('#txtIDNumber').val();
				var isnum_accNum = /^\d+$/.test(accountNumber);
				var isnum_cardNum = /^\d+$/.test(cardNumber);
				var isnum_accBalance = /^\d+$/.test(accountBalance);
				var isnum_phoneNum = /^\d+$/.test(phone);
				var isnum_idNum = /^\d+$/.test(idNumber);
				if ($.trim(sEmail).length == 0) {
					alert('Please enter valid email address');
				}
				if (!validateEmail(sEmail)||!(isnum_accBalance&&accountBalance>0)||!isnum_cardNum||!isnum_accNum||!isnum_phoneNum||!isnum_idNum) {
					alert('Please enter valid email address, account balance,card number, account number!');
				} else{
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
						$('#addPopUp').modal('hide');
						$scope.result=response.data;
						console.log($scope.result);
						if($scope.result.status=='OK'){
							$('#resultMessge').modal('show');
							$('#success').text($scope.result.message)
						}
						else{
							$('#resultMessge').modal('show');
							$('#fail').show();
							$('#succeed').hide();
							$('#error').text($scope.result.message)
						}
					}, function(error) {
						console.log(error);
					});
				}

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

			if($('#auth').text()=='Account Manager')
				$scope.showlist();
		})