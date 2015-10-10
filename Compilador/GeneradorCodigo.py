import os
import header_fix

class GeneradorNulo(object):
	def __init__(self):
		pass
	
	def no_generar(self):
		return self
	
	def finalizar(self):
		print "No se genero archivo ejecutable por encontrarse al menos un error"


EDI_INICIAL = [0xbf, 0x0, 0x0,0x0, 0x0]

def traduce(hexas):
	reduce(lambda x,y: x + chr(y) ,hexas, "")

class GeneradorLinux(object):
	def __init__(self, ruta_ejec):
		self.ruta = ruta_ejec
		self.ejecutable = open(ruta_ejec, "w")
		self.buffer = ""
		self._agregar_header()
		self._edi_inicial()
		
	
	def _flush(self):
		self.ejecutable.write(self.buffer)
		self.buffer = ""
	
	def _agregar_header(self):
		self.buffer += header_fix.HEADER
	
	def _edi_inicial(self):
		self.buffer += traduce(EDI_INICIAL)
	
	def no_generar(self):
		self.ejecutable.close()
		os.remove(self.ruta)
		return GeneradorNulo()
	
	def finalizar(self):
		self._flush()
		self.ejecutable.close()
		
	def __str__(self):
		return self.buffer

