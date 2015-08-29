OUT_DEFAULT = "program_log.mb"
ANULADOS = [" ", "\t"]
QUIEBRE = ["#", "\n"]
VACIO = ""

ERROR = -1,
IDENTIFICADOR_O_RESERVADA = 0
NUMERO = 1
ASIGNACION = 2
MENOR = 3
MAYOR = 4
IGUAL = 5
MENOR_IGUAL = 6
MAYOR_IGUAL = 7
DISTINTO = 8
PUNTO = 9
MAS = 10
MENOS = 11
MULTIPLICAR = 12
PUNTO_Y_COMA = 13
COMA = 14
DIVIDIR = 15
ABRIR_PARENTESIS = 16
CERRAR_PARENTESIS = 17
EOF = 18
ESPECIALES = {"+": MAS, "-": MENOS, "*": MULTIPLICAR, "/": DIVIDIR, ".": PUNTO, ",": COMA, ";": PUNTO_Y_COMA, "=": IGUAL, "(": ABRIR_PARENTESIS, ")": CERRAR_PARENTESIS }	
	
	
class AnalizadorLexico(object):
	
	def __init__(self, program_path, output_path = OUT_DEFAULT):
		self._leer_archivo(program_path)
		try:
			self.out = open(output_path, "w")
		except IOError:
			raise IOError("No se pudo crear el archivo de salida del analizador lexico")
		
		self.num_linea = 0
		self.quedan_lineas = True
		self._leer_linea()
		self.valor = None
	
	def _leer_archivo(self, program_path):
		self.lineas = []
		try:
			prog = open(program_path)
		except IOError:
			raise IOError("Archivo de programa no existe, o no se tienen permisos")
		for line in prog:
			self.lineas.append(line)
		prog.close()
	
	def _leer_linea(self):
		if len(self.lineas) == self.num_linea:
			self.quedan_lineas = False
			return
		
		self.linea_actual = self.lineas[self.num_linea]
		self.out.write(self.linea_actual)
		self.linea_actual = self.linea_actual.strip()
		self.num_linea += 1
	
	def obtener_valor_actual(self):
		return self.valor
	
	def obtener_simbolo(self):
		while self.quedan_lineas:
			for index, c in enumerate(self.linea_actual):
				if c in ANULADOS: continue
				if c in QUIEBRE: break
				
				if c.isalpha():
					self._obtener_id_o_reservada(index)
					return IDENTIFICADOR_O_RESERVADA
				
				if c.isdigit():
					self._obtener_numero(index)
					return NUMERO
				
				if c == ":":
					self._obtener_asignacion(index)
					return ASIGNACION if self.valor != None else ERROR
				
				if c == "<":
					self._obtener_menoridad(index)
					return MENOR_IGUAL if self.valor == "<=" else DISTINTO if self.valor == "<>" else MENOR
				if c == ">":
					self._obtener_mayoridad(index)
					return MAYOR_IGUAL if self.valor == ">" else MAYOR
				
				if c in ESPECIALES:
					self.valor = c
					self.linea_actual = self.linea_actual[index + 1:]
					return ESPECIALES[c]
				
				return ERROR
						
			self._leer_linea()
		return EOF
	
	def _obtener_completo(self, index, numero = False):
		formado = ""
		for i in range(index, len(self.linea_actual)):
			c = self.linea_actual[i]
			if c in ANULADOS or c in QUIEBRE or (numero and not c.isdigit()): break
			formado += c
			index += 1
		self.valor = formado
		self.linea_actual = self.linea_actual[index:]
		
	def _obtener_id_o_reservada(self, index):
		self._obtener_completo(index, numero=False)
	
	def _obtener_numero(self, index):
		self._obtener_completo(index, numero=True)
				
	def _obtener_combinaciones(self, index, primero, posibles_segundos):
		c = self.linea_actual[index]
		self.value = None
		if c != primero:
			return
		index += 1
		for i in range(index, len(self.linea_actual)):
			index += 1
			c = self.linea_actual[i]
			if c in ANULADOS: continue
			self.valor = primero + (c if c in posibles_segundos else "")
			if self.valor == primero: index -= 1
			break

		self.linea_actual = self.linea_actual[index:]
	
	def _obtener_menoridad(self, index):
		self._obtener_combinaciones(index, "<", [">", "="])
	
	def _obtener_mayoridad(self, index):
		self._obtener_combinaciones(index, ">", ["="])

	def _obtener_asignacion(self, index):
		self._obtener_combinaciones(index, ":", ["="])
		if self.valor != ":=": self.valor = None
	
	def terminar(self):
		self.out.close()
		
if __name__=="__main__":
	al = AnalizadorLexico("ejemplo.txt")
	while True:
		c = al.obtener_simbolo()
		if c == EOF: break
		print c
	al.terminar()
