$(document).ready(function () {
	 	$(function () {
                $('#datetimepicker_birthday_js,#datetimepicker_memberSince__js,#datetimepicker_searchBirthday_js').datetimepicker({
                        format: 'DD/MM/YYYY'
                });
            });
	 	$('#gender,#txtMemberSince').prop('disabled', 'disabled');
	 	$('.inputCustom,#passwordEye').prop('disabled',true);
	 	$('#btnUpdate').hide()
	 	console.log("I'm here")
	 	$('#btnEdit').click(function(){
	 		$('#addPopUp').css( 'cursor', 'context-menu' );
	 		$('#gender,#txtMemberSince').prop('disabled',false);
	 		$('.inputCustom,#passwordEye').prop('disabled',false);
	 		$('#addPopUp,#btnUpdate').show();
	 		$(this,'#btnSave').hide();
	 	});
	 	$('#btnUpdate').click(function(event){
	 		$('#addPopUp').css( 'cursor', 'progress' );
	 		$('#gender,#txtMemberSince').prop('disabled', 'disabled');
		 	$('.inputCustom,#passwordEye').prop('disabled',true);
		 	$('#btnUpdate').hide(1000);
		 	$('#btnEdit').show();

	 	});
	 	$(".glyphicon-eye-open").mousedown(function(){
                $("#txtPassword").attr('type','text');
            }).mouseup(function(){
            	$("#txtPassword").attr('type','password');
            }).mouseout(function(){
            	$("#txtPassword").attr('type','password');
            });
	 	$('#btnAddAccount').click(function(event){
	 		$(this).css( 'cursor', 'pointer' );
	 		$('#gender,#txtMemberSince').prop('disabled',false);
	 		$('.inputCustom,#passwordEye').prop('disabled',false);
	 		$('#btnUpdate,#btnEdit').hide();
	 		$('#btnSave').show();
	 		
	 		
	 	});
	 	$('#btnSave').click(function(){
	 		$('#addPopUp').css( 'cursor', 'progress' );
	 		$('#gender,#txtMemberSince').prop('disabled',true);
	 		$('.inputCustom,#passwordEye').prop('disabled',true);
	 		$(this).hide(1000);
	 		$('#btnUpdate').hide();
	 		$('#btnEdit').show();
	 	});
	 	$('#btnViewDetails').click(function(){
	 		$('#btnSave').hide();
	 	});
	 	function validateEmail(sEmail) {
	 		var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
	 		if (filter.test(sEmail)) {
	 			return true;
	 		}
	 		else {
	 			return false;
	 		}
	 	}
	 	$('#txtMail').mouseout(function() {
	 		var sEmail = $('#txtMail').val();
	 		if ($.trim(sEmail).length == 0) {
	 			alert('Please enter valid email address');
	 		}
	 		if (validateEmail(sEmail)) {
	 			$('#message_success').show();
	 			$('#message_fail').hide();
	 			
	 		}
	 		else {
	 			$('#message_fail').show();
	 			$('#message_success').hide();
	 			// e.preventDefault();
	 		}
	 	});
	 	$('#adminSearchFrame').click(function(){
	 		// var mytable=$('#myDataTable').dataTable()
	 		// mytable.fnDestroy();
			// $('#myDataTable').dataTable(response.data);
	 	});
	});