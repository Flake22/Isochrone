def create_age_and_sex(age_and_sex):
	pass

def create_family_composition(family_composition):
	pass

def create_commuters(commuters):
	pass

def generate_graphs(age_and_sex, family_composition, commuters):
	g1 = create_age_and_sex(age_and_sex)
	g2 = create_family_composition(family_composition)
	g3 = create_commuters(commuters)

	htmltext = """
	<script>
	function initMap() {{
	}}
	</script>
	"""

	return htmltext
