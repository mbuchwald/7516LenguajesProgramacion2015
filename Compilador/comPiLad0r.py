import sys
import AnalizadorLexico as lexico
import AnalizadorSemantico as semantico
import AnalizadorSintactico as sintactico

if __name__ == "__main__":
	output = open("salida.txt", "w")
	ruta = "Archivos/BIEN-09.PL0"
	if len(sys.argv) > 1:
		ruta = sys.argv[1]
	
	al = lexico.AnalizadorLexico(ruta, output)
	an_sem = semantico.AnalizadorSemantico(output)
	an_sintac = sintactico.AnalizadorSintactico(al, an_sem, output)
	an_sintac.parsear_programa()
	output.close()
