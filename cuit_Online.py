#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime

# Configuración
file_txt = "valores.txt"
result_name = "resultados"
error_name = "errores"
tiempo_espera = 4

base_url = "https://www.cuitonline.com/search/"
prefix_url = "https://www.cuitonline.com/"
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
fileresult_txt = f"{result_name}_{timestamp}.txt"
fileerror_txt = f"{error_name}_{timestamp}.txt"

def leer_terminos(file_path):
	with open(file_path, 'r') as file:
		return [re.sub(r'[.,_-]', '', line.strip()) for line in file if line.strip()]

def buscar_enlace(termino):
	url = f"{base_url}{termino}"
	print(f"Buscando: {url}")
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
		'Accept-Language': 'es-ES,es;q=0.9',
		'Referer': 'https://www.cuitonline.com/'
	}
	
	try:
		response = requests.get(url, headers=headers, timeout=10)
		response.raise_for_status()

		soup = BeautifulSoup(response.text, 'html.parser')
		enlaces = [prefix_url + a['href'] for a in soup.select('a[href*="detalle/"]')]
		if enlaces:
			for enlace in enlaces:
				print(f"[+] Persona encontrada: {enlace}")
				guardar_resultado(enlace, fileresult_txt)
		else:
			print(f"[-] No se encontraron resultados para '{termino}'.")
			guardar_error(termino, fileerror_txt)

	except requests.HTTPError as http_err:
		print(f"[x] Error al buscar '{termino}': {http_err}")
		guardar_error(termino, fileerror_txt)
	except Exception as e:
		print(f"[x] Excepción al buscar '{termino}': {e}")
		guardar_error(termino, fileerror_txt)

def guardar_resultado(enlace, file_path):
	with open(file_path, 'a') as result_file:
		result_file.write(enlace + '\n')

def guardar_error(termino, file_path):
	with open(file_path, 'a') as error_file:
		error_file.write(termino + '\n')

def main():
	terminos = leer_terminos(file_txt)
	for termino in terminos:
		buscar_enlace(termino)
		time.sleep(tiempo_espera)

	print(f"Enlaces guardados en {fileresult_txt}")
	print(f"Errores guardados en {fileerror_txt}")

if __name__ == "__main__":
	main()
