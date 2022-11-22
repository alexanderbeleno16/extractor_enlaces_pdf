import pandas as pd 
import PyPDF2
import re
import sys, datetime

class ExtractorRadicadoEnlace:
    
    def __init__(self, docPdf):
        self.docPdf = docPdf

    def extraerEnlaces(self, PDF):
        mylistEnlace = []
        dominio = 'http://visordocs.sic.gov.co:8080/'
        key = '/Annots'
        url = '/URI'
        ank = '/A'  
        paginas = PDF.getNumPages()        
        
        for page in range(paginas):
            # print( "--------------ENLACES--------------", "PAGINA: {}".format(page+1) )   
            paginaExtraida = PDF.getPage(page)
            ObjetoPaginaExtraida = paginaExtraida.getObject()
                    
            if key in ObjetoPaginaExtraida.keys():
                array_objetos = ObjetoPaginaExtraida[key]
                for obj in array_objetos:
                    try:
                        objeto = obj.getObject()
                        if url in objeto[ank].keys():
                            link=""
                            #ENLACES:
                            if ( re.search("^"+dominio+"*", objeto[ank][url]) ):
                                link = objeto[ank][url]    
                                if link not in mylistEnlace:
                                    # print( link )   
                                    mylistEnlace.append(link)  
                    except KeyError:
                        pass
        
        return mylistEnlace


    def extraerRadicados(self, PDF):
        mylistRadicadoTemp = []  
        mylistRadicado = []  
        can=0
        
        paginas = PDF.getNumPages()        
        for page in range(paginas):
            paginaExtraida = PDF.getPage(page)
            
            texto = paginaExtraida.extractText() #TODO EL TEXTO POR PAGINAS
            texto = str(texto).replace('\\','')
            texto = re.findall(r"([0-9][0-9][-][0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?)", texto) #<List>RADICADO ANIO Y RADICADO SEPARADO POR GUIONES. EJ: 22-426253 
            
            can += len(texto)
            mylistRadicadoTemp.append(texto)  
            
            # print( "\n\n <<<<<<<<< Hoja # ---> {} >>>>>>>>>>\n".format(page+1) , "Radicados: ", texto , "cantirdad: ", can)
                
            
        for radicados in mylistRadicadoTemp:
            if type(radicados)==list:
                for rad in radicados:
                    # if rad not in mylistRadicado:
                    mylistRadicado.append(rad)  
            
        return mylistRadicado


    def extraerEnlacesPrueba(self, PDF):
        mylistEnlace = []
        mylistRadicadoTemp = []  
        
        dominio = 'http://visordocs.sic.gov.co:8080/'
        key = '/Annots'
        url = '/URI'
        ank = '/A'  
        paginas = PDF.getNumPages()        
        
        for page in range(paginas):
            # print( "--------------ENLACES--------------", "PAGINA: {}".format(page+1) )   
            paginaExtraida = PDF.getPage(page)
            ObjetoPaginaExtraida = paginaExtraida.getObject()
            
            texto = paginaExtraida.extractText() #TODO EL TEXTO POR PAGINAS
            texto = str(texto).replace('\\','')
            texto = re.findall(r"([0-9][0-9][-][0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?)", texto) #<List>RADICADO ANIO Y RADICADO SEPARADO POR GUIONES. EJ: 22-426253 
            
            can += len(texto)
            mylistRadicadoTemp.append(texto)  
                    
            if key in ObjetoPaginaExtraida.keys():
                array_objetos = ObjetoPaginaExtraida[key]
                for obj in array_objetos:
                    try:
                        objeto = obj.getObject()
                        if url in objeto[ank].keys():
                            link=""
                            #ENLACES:
                            if ( re.search("^"+dominio+"*", objeto[ank][url]) ):
                                link = objeto[ank][url]    
                                if link not in mylistEnlace:
                                    # print( link )   
                                    mylistEnlace.append(link)  
                    except KeyError:
                        pass
        
        return mylistEnlace



    def abrirPDF(self):
        status = True 
        mylist = []
        content = {}
        
        try:
            # ARCHIVO_PDF = open(r'pdf_pruebas/ESTADO_212.pdf','rb')
            ARCHIVO_PDF = open(str(self.docPdf),'rb')
            
            PDF = PyPDF2.PdfFileReader(ARCHIVO_PDF, strict=False)

            # mylistRadicado = self.extraerRadicados(PDF)
            # mylistEnlace = self.extraerEnlaces(PDF)
            
            mylistEnlace = self.extraerEnlacesPrueba(PDF)
            # print( len(mylistRadicado) , len(mylistEnlace), mylistEnlace)
            
                
            # print("\n\nPagina(s) encontrada(s): {}".format(paginas))            
            # print("Links encontrado(s): {}".format(len(mylistEnlace)))   
        except FileNotFoundError as error:
            print('La ruta del documento especificado no se encontró...',error)
            
        
        




    
    
    
    
    
    
try:
    if(sys.argv[1] == ''):
        raise IndexError('Nombre del archivo vacio')
        
    file_name = sys.argv[1]
    
    # INSTANCIA DE LA CLASE CONVERTIDOR:
    conver = ExtractorRadicadoEnlace(file_name)

    conver.abrirPDF()
    
except IndexError:
        print('Se requiere el nombre del archivo',IndexError)
    