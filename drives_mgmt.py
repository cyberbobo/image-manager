import json

"""
Partant d'un JSON, explore récursivement le JSON et retourne un dictionnaire avec le champ 'name' en index et le champ 'uuid' en valeur
"""
def recursive_extraction(json_data):
	result = {}
	dict_data = json.loads(json_data)
	for i in dict_data['blockdevices']:
		result[i['name']]=i['uuid']
		if 'children' in i:
			for j in i['children']:
				result[j['name']]=j['uuid']
	return(result)