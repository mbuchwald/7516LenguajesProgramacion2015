import sys
import AnalizadorLexico
import AnalizadorSemantico

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
END = "end"
WRITE = "write"
WRITELN = "writeln"
READLN = "readln"

class AnalizadorSintactico(object):
	
	def __init__(self, scanner, semantico, output):
		self.out = output
		self.scanner = scanner
		self.semantico = semantico
	
	def _parsear_bloque(self, base = 0):
		desplazamiento = 0
		simbolo = self.scanner.obtener_simbolo()
		valor = self.scanner.obtener_valor_actual()
		#Analizamos la parte de constantes:
		if simbolo == AnalizadorLexico.RESERVADA and valor.lower() == CONST:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.IDENTIFICADOR:
					identificador = self.scanner.obtener_valor_actual()
					try:
						self.semantico.agregar_identificador(base,desplazamiento, identificador, AnalizadorSemantico.CONSTANTE)
						desplazamiento += 1
					except:
						continue #por ahora
				
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
		if simbolo == AnalizadorLexico.RESERVADA and valor.lower() == VAR:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.IDENTIFICADOR:
					identificador = self.scanner.obtener_valor_actual()
					try:
						self.semantico.agregar_identificador(base,desplazamiento, identificador, AnalizadorSemantico.VARIABLE)
						desplazamiento += 1
					except:
						continue #por ahora
					
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
		
		while simbolo == AnalizadorLexico.RESERVADA and self.scanner.obtener_valor_actual().lower() == PROCEDURE:
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.IDENTIFICADOR:
				output.write("Error Sintactico: declaracion de procedimiento no seguida de un identificador\n")
				continue
			identificador = self.scanner.obtener_valor_actual()
			
			try: 
				self.semantico.agregar_identificador(base,desplazamiento, identificador, AnalizadorSemantico.PROCEDIMIENTO)
				desplazamiento += 1
			except:
				continue #por ahora
			
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.PUNTO_Y_COMA:
				output.write("Error Sintactico: Luego de la identificacion de un procedimiento se esperaba por punto y coma (;)\n")
				continue
			self._parsear_bloque(base + desplazamiento) #ver como hacer para que quede asociado al identificador
			if self.scanner.obtener_tipo_actual() != AnalizadorLexico.PUNTO_Y_COMA:
				output.write("Error Sintactico: Luego de definir un procedimiento se esperaba por punto y coma (;)\n")
				continue
			simbolo = self.scanner.obtener_simbolo()
		
		self._parsear_proposicion(base, desplazamiento)
			
	def _parsear_proposicion(self, base, desplazamiento):
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo != AnalizadorLexico.IDENTIFICADOR and simbolo != AnalizadorLexico.RESERVADA:
			return
		
		valor = self.scanner.obtener_valor_actual()
		if valor.lower() == END:
			return
		
		if valor.lower() == CALL:
			simbolo = self.scanner.obtener_simbolo()
			identificador = self.scanner.obtener_valor_actual()
			
			if not self.semantico.invocacion_procedimiento_correcta(identificador, base, desplazamiento):
				return
			simbolo = self.scanner.obtener_simbolo()
				
		elif valor.lower() == IF:
			simbolo = self.scanner.obtener_simbolo()
			self._parsear_condicion(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.RESERVADA and self.scanner.obtener_valor_actual().lower() == THEN:
				simbolo = self.scanner.obtener_simbolo()
				self._parsear_proposicion(base, desplazamiento)
			else:
				self.out.write("Error Sintactico: Se esperaba un 'then' luego de la condicion de un 'if'\n")
				self.scanner.frenar()
		elif valor.lower() == WHILE:
			simbolo = self.scanner.obtener_simbolo()
			self._parsear_condicion(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.RESERVADA and self.scanner.obtener_valor_actual().lower() == DO:
				simbolo = self.scanner.obtener_simbolo()
				self._parsear_proposicion(base, desplazamiento)
			else:
				self.out.write("Error Sintactico: Se esperaba un 'do' luego de la condicion de un 'while'\n")
		elif valor.lower() == BEGIN:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				self._parsear_proposicion(base, desplazamiento)
				simbolo = self.scanner.obtener_tipo_actual()
				if simbolo == AnalizadorLexico.RESERVADA and self.scanner.obtener_valor_actual().lower() == END:
					simbolo = self.scanner.obtener_simbolo()
					break
				elif simbolo != AnalizadorLexico.PUNTO_Y_COMA:
					self.out.write("Error Sintactico: Se esperaba un END o punto y coma (;) luego de una proposicion de un Begin\n")
					#indicar que no se genera codigo
					#Asumimos que venia un ;
					if simbolo != AnalizadorLexico.COMA: 
						self.scanner.frenar()
					
		elif valor.lower() == WRITE or valor.lower() == WRITELN:
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.ABRIR_PARENTESIS:
				if valor == WRITE:
					self.out.write("Error Sintactico: Se esperaba un parentesis luego de write \n")
				return
			simbolo = self.scanner.obtener_simbolo()
			if simbolo == AnalizadorLexico.CADENA:
				#hacemos algo con esto
				if self.scanner.error_en_cadena:
					pass #indicamos que no se puede generar codigo
				valor = self.scanner.obtener_valor_actual()
				simbolo = self.scanner.obtener_simbolo()
			else:
				self._parsear_expresion(base, desplazamiento)
				
			while self.scanner.obtener_tipo_actual() == AnalizadorLexico.COMA:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.CADENA:
					#hacemos algo con esto
					valor = self.scanner.obtener_valor_actual()
					simbolo = self.scanner.obtener_simbolo()
				else:
					self._parsear_expresion(base, desplazamiento)
				
			if self.scanner.obtener_tipo_actual() != AnalizadorLexico.CERRAR_PARENTESIS:
				self.out.write("Error Sintactico: Se esperaba un cierre de parentesis luego de write \n")
			simbolo = self.scanner.obtener_simbolo()	
			
		elif valor.lower() == READLN:
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.ABRIR_PARENTESIS:
				self.out.write("Error Sintactico: Se esperaba un parentesis luego de readln \n")
				return
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.IDENTIFICADOR:
				self.out.write("Error Sintactico: Se esperaba identificador dentro de readln \n")
				return
			identificador = self.scanner.obtener_valor_actual()
			
			self.semantico.lectura_correcta(identificador, base, desplazamiento)
						
			simbolo = self.scanner.obtener_simbolo()
			while simbolo == AnalizadorLexico.COMA:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo != AnalizadorLexico.IDENTIFICADOR:
					self.out.write("Error Sintactico: Se esperaba identificador dentro de readln \n")
					return
				simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.CERRAR_PARENTESIS:
				self.out.write("Error Sintactico: Se esperaba cierre de parentesis luego de readln \n")
			simbolo = self.scanner.obtener_simbolo()
		else:
			if simbolo != AnalizadorLexico.IDENTIFICADOR:
				self.out.write("Error Sintactico: Se esperaba variable en asignacion, se encuentra la palabra reservada: " + self.scanner.obtener_valor_actual() + "\n")
				return
			identificador = self.scanner.obtener_valor_actual()
			
			if self.semantico.asignacion_correcta(identificador, base, desplazamiento):
				pass #indicar que no se genera codigo		
			
			simbolo = self.scanner.obtener_simbolo()
			if simbolo != AnalizadorLexico.ASIGNACION:
				self.out.write("Error Sintactico: Esperada asignacion luego de variable\n")
				#indicar que no se genera codigo
				
			simbolo = self.scanner.obtener_simbolo()
			self._parsear_expresion(base, desplazamiento)
		
	def _parsear_condicion(self, base, desplazamiento):
		simbolo = self.scanner.obtener_tipo_actual()
		valor = self.scanner.obtener_valor_actual()
		if valor == ODD:
			simbolo = self.scanner.obtener_simbolo()
			self._parsear_expresion(base, desplazamiento)
		else:
			self._parsear_expresion(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.IGUAL or simbolo == AnalizadorLexico.MAYOR or simbolo == AnalizadorLexico.MAYOR_IGUAL or simbolo == AnalizadorLexico.MENOR or simbolo == AnalizadorLexico.MENOR_IGUAL or simbolo == AnalizadorLexico.DISTINTO:
				simbolo = self.scanner.obtener_simbolo()
				self._parsear_expresion(base, desplazamiento)
			else:
				self.out.write("Error Sintactico: Se esperaba simbolo de comparacion en comparacion")
					
	def _parsear_expresion(self, base, desplazamiento):
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo == AnalizadorLexico.MAS or simbolo == AnalizadorLexico.MENOS:
			simbolo = self.scanner.obtener_simbolo()
		while True:
			self._parsear_termino(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.MAS or simbolo == AnalizadorLexico.MENOS:
				simbolo = self.scanner.obtener_simbolo()
			else:
				return
				
	def _parsear_termino(self, base, desplazamiento):
		while True:
			self._parsear_factor(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.MULTIPLICAR or simbolo == AnalizadorLexico.DIVIDIR:
				simbolo = self.scanner.obtener_simbolo()
			else:
				return
				
	def _parsear_factor(self, base, desplazamiento):
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo == AnalizadorLexico.NUMERO:
			simbolo = self.scanner.obtener_simbolo()
		elif simbolo == AnalizadorLexico.IDENTIFICADOR:
			identificador = self.scanner.obtener_valor_actual()
			if not self.semantico.factor_correcto(identificador, base, desplazamiento):
				return
			simbolo = self.scanner.obtener_simbolo()			
		elif simbolo == AnalizadorLexico.ABRIR_PARENTESIS:
			simbolo = self.scanner.obtener_simbolo()
			self._parsear_expresion(base, desplazamiento)
			simbolo = self.scanner.obtener_tipo_actual()
			if simbolo == AnalizadorLexico.CERRAR_PARENTESIS:
				simbolo = self.scanner.obtener_simbolo()
			else:
				self.out.write("Error Sintactico: Cierre de parentesis faltante")
		else:
			self.out.write("Error Sintactico: Identificador no esperado")
				
			
	def parsear_programa(self):
		self._parsear_bloque()
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo != AnalizadorLexico.PUNTO:
			output.write("Error Sintactico: Se esperaba punto (.) de finalizacion de programa\n")
		


if __name__ == "__main__":
	output = open("salida.txt", "w")
	ruta = "Archivos/BIEN-09.PL0"
	if len(sys.argv) > 1:
		ruta = sys.argv[1]
	
	al = AnalizadorLexico.AnalizadorLexico(ruta, output)
	an_sem = AnalizadorSemantico.AnalizadorSemantico(output)
	an_sintac = AnalizadorSintactico(al, an_sem, output)
	an_sintac.parsear_programa()
	output.close()
