import os
import header_fix

class GeneradorNulo(object):
	def __init__(self):
		pass
	
	def no_generar(self):
		return self
		
	def factor_numero(self, valor):
		pass
		
	def factor_variable(self, num_var):
		pass
	
	def multiplicar(self):
		pass
	
	def dividir(self):
		pass
	
	def finalizar(self):
		print "No se genero archivo ejecutable por encontrarse al menos un error"


EDI_INICIAL = [0xbf, 0x0, 0x0,0x0, 0x0]
PUSH_EAX = 0x50
MOV_EAX_CONS = [0xb8]
MOV_EAX_VAR = [0x8B, 0x87]
POP_EAX = 0x58
POP_EBX = 0x5B
IMUL_EBX = [0xF7, 0xEB]
DIVISION = [0x93, 0x99, 0xF7, 0xFB]

def traduce(hexas):
	return reduce(lambda x,y: x + chr(y) ,hexas, "")
	
def endian(numero):
	hexa = str(hex(numero))[2:]
	hexa = reduce(lambda x,y: x+y, ["0" for i in range(8 - len(hexa))], "") + hexa
	hexa = [hexa[i*2] + hexa[i*2 +1] for i in range(4)]
	hexa.reverse()
	return map(lambda x: int(x, 16), hexa)

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
	
	def _push_eax(self):
		self.buffer += chr(PUSH_EAX)
	
	def factor_numero(self, valor):
		valor = int(valor)
		self.buffer += traduce(MOV_EAX_CONS + endian(valor))
		self._push_eax()
	
	def factor_variable(self, num_var):
		self.buffer += traduce(MOV_EAX_VAR + endian(num_var))
		self._push_eax()
		
	def multiplicar(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + IMUL_EBX)
		self._push_eax()
		
	def dividir(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + DIVISION)
		self._push_eax()
		
	def __str__(self):
		return self.buffer

