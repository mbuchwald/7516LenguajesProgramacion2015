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
	
	def negar(self):
		pass
	
	def sumar(self):
		pass
	
	def restar(self):
		pass
	
	def finalizar(self, cant_variables):
		print "No se genero archivo ejecutable por encontrarse al menos un error"

BYTES_POR_VARIABLE = 4
COMPLEMENTO = 2**32 
POS_RUTINA_SALIDA = 768
EDI = 0xbf
EDI_INICIAL = [0x0, 0x0,0x0, 0x0]
PUSH_EAX = 0x50
MOV_EAX_CONS = [0xb8]
MOV_EAX_VAR = [0x8B, 0x87]
POP_EAX = 0x58
POP_EBX = 0x5B
IMUL_EBX = [0xF7, 0xEB]
DIVISION = [0x93, 0x99, 0xF7, 0xFB] #93 99?
NEG_EAX = [0xF7, 0xD8]
ADD = [0x01, 0xD8]
SUB = [0x93, 0x29, 0xD8] #no se para que el 93
JMP = [0xe9]

def traduce(hexas):
	return reduce(lambda x,y: x + chr(y) ,hexas, "")
	
def endian(numero):
	hexa = str(hex(numero))[2:]
	hexa = reduce(lambda x,y: x+y, ["0" for i in range(8 - len(hexa))], "") + hexa
	hexa = [hexa[i*2] + hexa[i*2 +1] for i in range(4)]
	hexa.reverse()
	return map(lambda x: int(x, 16), hexa)
	
def salto(adonde, donde_estoy):
	return COMPLEMENTO + adonde - donde_estoy

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
		self.pos_edi = len(self.buffer) - 1
		self.buffer += traduce([EDI] + EDI_INICIAL)
	
	def no_generar(self):
		self.ejecutable.close()
		os.remove(self.ruta)
		return GeneradorNulo()
	
	def finalizar(self, cant_variables):
		self.buffer += traduce(JMP + endian(salto(POS_RUTINA_SALIDA ,(len(self.buffer) + 5))))
		self.buffer = self.buffer[:self.pos_edi] + traduce([EDI] + endian(header_fix.VIRTUAL_ADDRESS + len(self.buffer))) + self.buffer[self.pos_edi + 5:]
		self.buffer += traduce([0 for i in range(cant_variables * BYTES_POR_VARIABLE)])
		self._flush()
		self.ejecutable.close()
	
	def _push_eax(self):
		self.buffer += chr(PUSH_EAX)
	
	def factor_numero(self, valor):
		valor = int(valor)
		self.buffer += traduce(MOV_EAX_CONS + endian(valor))
		self._push_eax()
	
	def factor_variable(self, num_var):
		self.buffer += traduce(MOV_EAX_VAR + endian(BYTES_POR_VARIABLE * num_var))
		self._push_eax()
		
	def multiplicar(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + IMUL_EBX)
		self._push_eax()
		
	def dividir(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + DIVISION)
		self._push_eax()
		
	def negar(self):
		self.buffer += traduce([POP_EAX] + NEG_EAX)
		self._push_eax()
	
	def sumar(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + ADD)
		self._push_eax()
	
	def restar(self):
		self.buffer += traduce([POP_EAX, POP_EBX] + SUB)
		self._push_eax()
		
	def __str__(self):
		return self.buffer

