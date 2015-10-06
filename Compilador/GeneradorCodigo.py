import os
import header_fix

class GeneradorNulo(object):
	def __init__(self):
		pass
	
	def no_generar(self):
		return self
	
	def finalizar(self):
		print "No se genero archivo ejecutable por encontrarse al menos un error"

class GeneradorLinux(object):
	def __init__(self, ruta_ejec):
		self.ruta = ruta_ejec
		self.ejecutable = open(ruta_ejec, "w")
		self.buffer = ""
		self._agregar_header()
	
	def _agregar_header(self):
		self.buffer += header_fix.header
	
	def no_generar(self):
		self.ejecutable.close()
		os.remove(self.ruta)
		return GeneradorNulo()
	
	def finalizar(self):
		self.ejecutable.close()

