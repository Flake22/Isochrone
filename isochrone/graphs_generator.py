def create_age_and_sex(age_and_sex):
	t = """
	    var config = {
	    type: 'pie',
	    data: {
	        datasets: [{
	            data: [
	                0,
	                0,
	    """
	for x in xrange(0,len(age_and_sex)-2):
		t+=str(age_and_sex[x])+""","""

	t +="""],
	                backgroundColor: [
	                "#FF4EF0",
	                "#5795FF",
	                "#39D131",
	                "#FFF126",
	                "#FF6026",
	                "#FF6026",
	                "#FFF126",
	                "#39D131",
	            ],
	        }, {
	            data: [
	    """
	for x in xrange(len(age_and_sex)-2,len(age_and_sex)):
		t+=str(age_and_sex[x])+""","""

	t +="""],
	                backgroundColor: [
	                "#FF4EF0",
	                "#5795FF",
	            ],
	        }],
	        labels: [
	            "Female",
	            "Male",
	            "Female 0-29",
	            "Female 30-54",
	            "Female >55",
	            "Male >55",
	            "Male 30-54",
	            "Male 0-29",
	        ]
	    },
	    options: {
	        responsive: true
	        
	    }
	};
	"""

	return t

def create_family_composition(family_composition):
	t = """
	var config2 = {
	    type: 'pie',
	    data: {
	        datasets: [{
	            data: [
	    """
	for x in xrange(0,len(family_composition)):
		t+=str(family_composition[x])+""","""

	t +="""],
	                backgroundColor: [
	                "#ff0000",
	                "#ff8000",
	                "#ffff00",
	                "#bfff00",
	                "#40ff00",
	                "#00ff80",
	            ],
	        }],
	        labels: [
	            "1",
	            "2",
	            "3",
	            "4",
	            "5",
	            "6 or more",
	        ]
	    },
	    options: {
	        responsive: true
	        
	    }
	};
	"""

	return t

def create_commuters(commuters):
	t = """
	var config3 = {
	    type: 'pie',
	    data: {
	        datasets: [{
	            data: [
	    """
	for x in xrange(0,len(commuters)):
		t+=str(commuters[x])+""","""

	t +="""],
	                backgroundColor: [
	                "#0066ff",
	                "#ff6600",
	            ],
	        }],
	        labels: [
	            "inside town",
	            "outside town",
	        ]
	    },
	    options: {
	        responsive: true
	        
	    }
	};
	"""
	return t

def generate_graphs(age_and_sex, family_composition, commuters):
	g1 = create_age_and_sex(age_and_sex)
	g2 = create_family_composition(family_composition)
	g3 = create_commuters(commuters)

	htmlgraphs= """
		<form action="#" method="get">
    <br>
	
	<!--Container for graph 01-->
	<div class="container-full form-group">
	
		<div class="row">
			<div class="col-lg-12">
			
				<div class="panel panel-default">
					
					<div class="panel-heading">
						<h4 class="panel-title">
							Population by age and gender
						</h4>
					</div>
					
					<div id="menu-part">
						
						<center>
						<div id="canvas-holder" style="width:87%">
    						<canvas id="chart-area-1" width="400" height="550" />
						</div>
						</center>
						
						<div id="legend">
							
						</div>
						
					</div>
				</div>
			</div>
		</div>
	
    <br>
	
	
	
	<!--Row for graph 02-->
	<div class="row">
			<div class="col-lg-12">
			
				<div class="panel panel-default">
					
					<div class="panel-heading">
						<h4 class="panel-title">
							Families by components
						</h4>
					</div>
					
					<div id="menu-part">
						
						<center>
						<div id="canvas-holder" style="width:87%">
    						<canvas id="chart-area-2" width="400" height="500" />
						</div>
						</center>
						
					</div>
				</div>
			</div>
		</div>
		
		<br>
		
	<!--Row for graph 03-->
	<div class="row">
		<div class="col-lg-12">
		
			<div class="panel panel-default">
				
				<div class="panel-heading">
					<h4 class="panel-title">
						Average daily movements
					</h4>
				</div>
				
				<div id="menu-part">
					
						<center>
						<div id="canvas-holder" style="width:87%">
    						<canvas id="chart-area-3" width="400" height="500" />
						</div>
						</center>
					
				</div>
			</div>
		</div>
	</div>
		
	
	
	<br>
	
	<div class="row">
		<div class="col-md-5 col-md-offset-2">
	
			<div id="centered">
				
				<button id="buttonBackToMenu" class="btn btn-primary btn-lg"><span class="glyphicon glyphicon-backward"></span> Back to menu</button>
				
				
			</div>
			
		</div>
	</div>
	
	</div>
	</form>

	<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.js"></script>
	<script>
	"""
	
	htmlgraphs +=g1+g2+g3
	    

	htmlgraphs+="""
	Chart.defaults.global.legend.position = 'bottom';
	Chart.defaults.global.legend.labels.boxWidth = 3;
	Chart.defaults.global.legend.labels.fontSize = 10;
	Chart.defaults.global.legend.labels.padding = 3;
	Chart.defaults.global.legend.labels.usePointStyle = true;
	//Chart.defaults.global.legend.display = false;
	var ctx = document.getElementById("chart-area-1").getContext("2d");
	var myPie = new Chart(ctx, config);
	var ctx2 = document.getElementById("chart-area-2").getContext("2d");
	var myPie2 = new Chart(ctx2, config2);
	var ctx3 = document.getElementById("chart-area-3").getContext("2d");
	var myPie3 = new Chart(ctx3, config3);
	
	//document.getElementById('legend').innerHTML = myPi.generateLegend();
	</script>
	"""

	return htmlgraphs