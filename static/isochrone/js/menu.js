
$(document).ready(function(){
	$('#buttonEnabled').click(function(){
	  $('#buttonEnabled').hide();
	  $('#buttonDisabled').show();
	});

	$('#dismissModalButton').click(function(){
	  $('#messageModal').modal('hide');
	});
	   
	   
   	$('#angles').slider({
		formatter: function(value) {
			return 'Current value: ' + value;
	}
	});
	$("#angles").slider();
		$("#angles").on("slide", function(slideEvt) {
			$("#anglesSliderVal").text(slideEvt.value);
		});

	$('#tolerance').slider({
		formatter: function(value) {
			return 'Current value: ' + value;
		}
	});
	$("#tolerance").slider();
		$("#tolerance").on("slide", function(slideEvt) {
			$("#toleranceSliderVal").text(slideEvt.value);
		});


	$('#ex1').slider({
		formatter: function(value) {
			return 'Current value: ' + value;
		}
	});
	$("#slider").slider();
		$("#slider").on("slide", function(slideEvt) {
			$("#sliderSliderVal").text(slideEvt.value);
		});

	});




