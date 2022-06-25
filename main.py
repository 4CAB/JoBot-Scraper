import requests
from re import findall

"""
IMPORTANTE
El formato del HTML
de linkedin cambia con cada requests
"""

def Remove(data:list[tuple]) -> list:
	"""
	Elimina los vacios dentro de las tuplas que estan dentro de la lista
	"""
	new_data = [i[0] if i[0] else i[1] for i in data]

	return new_data

def Extract(response) -> tuple:
	"""
	Extrae titulo, nombre de la empresa y link del perfil del trabajo
	"""
	titulo = findall(r'base-search-card__title">(\s+.+\s+)<\/h3>', response.text)
	job_titulo = [i.strip() for i in titulo]
	link_to_job = findall(r'href="(.+?)\?refId', response.text)

	# Devuelve [(True, False), [False, True]] aleatoriamente
	nombre_empresa = findall(r'base-search-card__subtitle".+?\s+<a.+>\s+(.+?)\s+<\/a>|.+?>\s+(.+?)\s+<\/h4>', response.text)
	nombre_empresa = Remove(nombre_empresa)

	return(job_titulo, nombre_empresa, link_to_job)

def Packager(elements:tuple) -> tuple:
	"""
	Organiza los datos de la tupla

	((job_titulo, nombre_empresa, link_to_job), . . .)
	"""
	new_elements = ()
	for i in range(len(elements[0])):
		new_elements += (elements[0][i], elements[1][i], elements[2][i])

	return new_elements

def main(keywords, location):
	r = requests.get(f'https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')
	data = Extract(r)

	return Packager(data)

"""if __name__ == '__main__':
	main('python', 'Colombia')"""