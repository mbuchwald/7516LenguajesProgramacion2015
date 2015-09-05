import AnalizadorLexico

CONST = "const"
VAR = "var"
PROCEDURE = "procedure"

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
				output.write("Luego de definir un procedimiento se esperaba por punto y coma (;)\n")
				continue
			simbolo = self.scanner.obtener_simbolo()
			
	
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
