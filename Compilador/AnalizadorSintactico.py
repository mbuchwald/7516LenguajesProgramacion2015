import AnalizadorLexico

CONST = "const"
VAR = "var"
PROCEDURE = "procedure"
CALL = "call"
IF = "if"
WHILE = "while"
BEGIN = "begin"
THEN = "then"
DO = "do"
ODD = "odd"

class AnalizadorSintactico(object):
	
	def __init__(self, scanner, output):
		self.out = output
		self.scanner = scanner
	
	def _parsear_bloque(self):
		simbolo = self.scanner.obtener_simbolo()
		valor = self.scanner.obtener_valor_actual()
		#Analizamos la parte de constantes:
		if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA and valor == CONST:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
					identificador = self.scanner.obtener_valor_actual()
					#TODO: mandar al analizador semantico para ver que sea correcto el identificador!
				
					simbolo = self.scanner.obtener_simbolo()
					if simbolo == AnalizadorLexico.IGUAL:
						simbolo = self.scanner.obtener_simbolo()
						if simbolo == AnalizadorLexico.NUMERO:
							valor = self.scanner.obtener_valor_actual()
							#TODO: asignarle el valor al identificador
							
							simbolo = self.scanner.obtener_simbolo()
							if simbolo == AnalizadorLexico.PUNTO_Y_COMA:
								simbolo = self.scanner.obtener_simbolo()
								break
							elif simbolo != AnalizadorLexico.COMA:
								output.write("Error Sintactico: Se esperaba punto y coma (;) o coma (,) luego de declaracion de constante\n")
								break
						else:
							output.write("Error Sintactico: asignacion de constante a un valor no numerico\n")
							break
					else:
						output.write("Error Sintactico: asignacion de constante esperada (=)\n")
						break
				else:
					output.write("Error Sintactico: declaracion de constante no seguida de un identificador\n")
					break
					
		valor = self.scanner.obtener_valor_actual()
		if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA and valor == VAR:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
					identificador = self.scanner.obtener_valor_actual()
					#TODO: definir identificador como variable, analizador que no sea reservada ni constante ni variable, etc...
					simbolo = self.scanner.obtener_simbolo()
					if simbolo == AnalizadorLexico.PUNTO_Y_COMA:
						simbolo = self.scanner.obtener_simbolo()
						break
					elif simbolo != AnalizadorLexico.COMA:
						output.write("Error Sintactico: Se esperaba punto y coma (;) o coma (,) luego de declaracion de variable\n")
						break
				else:
					output.write("Error Sintactico: declaracion de variable no seguida de un identificador\n")
					break
							
		while simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA and self.scanner.obtener_valor_actual() == PROCEDURE:
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
				output.write("Error Sintactico: declaracion de procedimiento no seguida de un identificador\n")
				continue
			identificador = self.scanner.obtener_valor_actual()
			#TODO: definir identificador como procedimiento + validaciones
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.PUNTO_Y_COMA:
				output.write("Error Sintactico: Luego de la identificacion de un procedimiento se esperaba por punto y coma (;)\n")
				continue
			self._parsear_bloque() #ver como hacer para que quede asociado al identificador
			if self.scanner.obtener_tipo_actual() != AnalizadorLexico.PUNTO_Y_COMA:
				output.write("Error Sintactico: Luego de definir un procedimiento se esperaba por punto y coma (;)\n")
				continue
			simbolo = self.scanner.obtener_simbolo()
			
		self._parsear_proposicion()
			
	def _parsear_proposicion(self):
		simbolo = self.parser.obtener_tipo_actual()
		if simbolo != AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
			return
		valor = self.parser.obtener_valor_actual()
		if valor == CALL:
			simbolo = self.parser.obtener_tipo_actual()
			identificador = self.parser.obtener_valor_actual()
			#Validar que el identificador sea de un procedimiento
		elif valor == IF:
			simbolo = self.parser.obtener_simbolo()
			self._parsear_condicion()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == IDENTIFICADOR_O_RESERVADA and self.parser.obtener_valor_actual() == THEN:
				simbolo = self.parser.obtener_simbolo()
				self._parsear_proposicion()
			else:
				self.output.write("Error Sintactico: Se esperaba un 'then' luego de la condicion de un 'if'")
		elif valor == WHILE:
			simbolo = self.parser.obtener_simbolo()
			self._parsear_condicion()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == IDENTIFICADOR_O_RESERVADA and self.parser.obtener_valor_actual() == DO:
				simbolo = self.parser.obtener_simbolo()
				self._parsear_proposicion()
			else:
				self.output.write("Error Sintactico: Se esperaba un 'do' luego de la condicion de un 'while'")
		elif valor == BEGIN:
			while True:
				simbolo = self.parser.obtener_simbolo()
				self._parsear_proposicion()
				simbolo = self.parser.obtener_tipo_actual()
				if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA and self.parser.obtener_valor_actual() == END:
					break
				elif simbolo != AnalizadorLexico.PUNTO_Y_COMA:
					self.output.write("Error Sintactico: Se esperaba un END o punto y coma (;) luego de una proposicion de un Begin")
					break
		else:
			#TODO Validar identificador como variable
			simbolo = self.parser.obtener_simbolo()
			if simbolo != ASIGNACION:
				self.output.write("Error Sintactico: Esperada asignacion luego de variable\n")
				return
			simbolo = self.parser.obtener_simbolo()
			self._parsear_expresion()
		
	def _parsear_condicion(self):
		simbolo = self.parser.obtener_tipo_actual()
		if simbolo == ODD:
			simbolo = self.parser.obtener_simbolo()
			self._parsear_expresion()
		else:
			self._parsear_expresion()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.IGUAL or simbolo == AnalizadorLexico.MAYOR or simbolo == AnalizadorLexico.MAYOR_IGUAL or simbolo == AnalizadorLexico.MENOR or simbolo == AnalizadorLexico.MENOR_IGUAL or simbolo == AnalizadorLexico.DISTINTO:
				simbolo = self.parser.obtener_simbolo()
				self._parsear_expresion()
			else:
				self.output.write("Error Sintactico: Se esperaba simbolo de comparacion en comparacion")
					
	def _parsear_expresion(self):
		simbolo = self.parser.obtener_tipo_actual()
		if simbolo == AnalizadorLexico.MAS or if simbolo == AnalizadorLexico.MENOS:
			simbolo = self.parser.obtener_simbolo()
		while True:
			self._parsear_termino()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.MAS or if simbolo == AnalizadorLexico.MENOS:
				simbolo = self.parser.obtener_simbolo()
			else:
				return
				
	def _parsear_termino(self):
		while True:
			self._parsear_factor()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.MULTIPLICAR or simbolo == AnalizadorLexico.DIVIDIR:
				simbolo = self.parser.obtener_simbolo()
			else:
				return
				
	def _parsear_factor(self):
		simbolo = self.parser.obtener_tipo_actual()
		if simbolo == AnalizadorLexico.NUMERO:
			simbolo = self.parser.obtener_simbolo()
		elif simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
			#Validar que sea constante o variable
			simbolo = self.parser.obtener_simbolo()
		elif simbolo == AnalizadorLexico.ABRIR_PARENTESIS:
			simbolo = self.parser.obtener_simbolo()
			self._parsear_expresion()
			simbolo = self.parser.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.CERRAR_PARENTESIS:
				simbolo = self.parser.obtener_simbolo()
			else:
				self.output.write("Error Sintactico: Cierre de parentesis faltante")
		else:
			self.output.write("Error Sintactico: Identificador no esperado")
				
			
	def parsear_programa(self):
		self._parsear_bloque()
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo != AnalizadorLexico.PUNTO:
			output.write("Error Sintactico: Se esperaba punto (.) de finalizacion de programa\n")
		


if __name__ == "__main__":
	output = open("salida.txt", "w")
	al = AnalizadorLexico.AnalizadorLexico("ejemplo.txt", output)
	an_sintac = AnalizadorSintactico(al, output)
	an_sintac.parsear_programa()
	output.close()
