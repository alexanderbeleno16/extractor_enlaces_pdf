import pandas as pd 
import PyPDF2
import re
import sys, datetime
import io
import urllib.request


class ExtractorRadicadoEnlace:
    
    def __init__(self, docPdf, opcion):
        self.docPdf = docPdf
        self.opcion = opcion

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
                        # print( objeto ) 
                        # continue
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
            # if type(radicados)==list:
            for rad in radicados:
                # if rad not in mylistRadicado:
                mylistRadicado.append(rad)  
            
        return mylistRadicado


    def extraerProvidencia(self, PDF):
            mylistProvideciaTemp = []  
            mylistProvidencia = []  
            can=0
            
            paginas = PDF.getNumPages()        
            for page in range(paginas):
                paginaExtraida = PDF.getPage(page)
                
                texto = paginaExtraida.extractText() #TODO EL TEXTO POR PAGINAS
                texto = str(texto).replace('\\','')
                texto = re.findall(r"([0-9][0-9][0-9][0-9][0-9][0-9]?)", texto) #<List>RADICADO ANIO Y RADICADO SEPARADO POR GUIONES. EJ: 22-426253 
                
                can += len(texto)
                mylistProvideciaTemp.append(texto)  
                
                # print( "\n\n <<<<<<<<< Hoja # ---> {} >>>>>>>>>>\n".format(page+1) , "providencias: ", texto , "cantirdad: ", can)
                    
                
            for providencias in mylistProvideciaTemp:
                # if type(providencias)==list:
                for rad in providencias:
                    # if rad not in mylistProvidencia:
                    mylistProvidencia.append(rad)  
                
            mylistProvidencia=list(filter(lambda a: a != '018000', mylistProvidencia))
            # mylistProvidencia = set(mylistProvidencia)
            return mylistProvidencia






    def abrirPDFlink(self):
        try:
            req = urllib.request.Request(self.docPdf, headers={'User-Agent' : "Magic Browser"})
            remote_file = urllib.request.urlopen(req).read()
            ARCHIVO_PDF_REMOTE = io.BytesIO(remote_file)
            PDF_REMOTE = PyPDF2.PdfFileReader(ARCHIVO_PDF_REMOTE, strict=False)

            self.menuOpcion(PDF_REMOTE)
            
        except FileNotFoundError as error:
            print('URL: La ruta del documento especificado no se encontró...',error)

    
    def abrirPDF(self):
        try:
            ARCHIVO_PDF = open(str(self.docPdf),'rb')
            PDF = PyPDF2.PdfFileReader(ARCHIVO_PDF, strict=False)
            
            self.menuOpcion(PDF)
            
        except FileNotFoundError as error:
            print('La ruta del documento especificado no se encontró...',error)
            
    
    def menuOpcion(self, PDF):
        if int(self.opcion) == 1:
            mylistRadicado = self.extraerRadicados(PDF)
            print( mylistRadicado , len(mylistRadicado) )
            
        elif int(self.opcion) == 2:
            mylistEnlace   = self.extraerEnlaces(PDF)
            print( mylistEnlace , len(mylistEnlace) )
            
        elif int(self.opcion) == 3:
            mylistRadicado = self.extraerRadicados(PDF)
            mylistEnlace   = self.extraerEnlaces(PDF)
            print( mylistRadicado , mylistEnlace )
            print( len(mylistRadicado) , len(mylistEnlace))
            
        elif int(self.opcion) == 4:
            mylistProvidencia   = self.extraerProvidencia(PDF)
            print( mylistProvidencia , len(mylistProvidencia) )
            

        # for i, radicado in enumerate(mylistRadicado):
            #     print(i+1, radicado, mylistEnlace[i])
        # print( mylistRadicado , mylistEnlace)
        

    
    
    

# python .\extractorSic_v2.class.py <<parametro#1: path/URL>> <<parametro#2: option>> 
# option: (1, 2, 3)
# 1: Extraer solo radicados
# 2: Extraer solo enlaces
# 3: Extraer radicados y enlaces
# 4: Extraer providencia <<Temporal>>
try:
    # print( type(sys.argv[2]) )
    msg = "\nLa opción < {} > no existe. \n".format(sys.argv[2])
    msg += "OPCIONES: \n"
    msg += "< 1 > Extraer solo radicados \n"
    msg += "< 2 > Extraer solo enlaces \n"
    msg += "< 3 > Extraer radicados y enlaces \n"
    
    if(sys.argv[1] == ''):
        raise IndexError('Nombre del archivo vacio (0)')
    
    if(sys.argv[2] == ''):
        raise IndexError(msg)
    
    file_name = sys.argv[1]
    opcion    = sys.argv[2]
    
    if (re.findall(r"([a-zA-Z])|([5-9])", opcion) ):
        print(msg)
    else:
        # INSTANCIA DE LA CLASE CONVERTIDOR:
        conver = ExtractorRadicadoEnlace(file_name, opcion)
        if ( re.search("^http*", file_name) ):
            conver.abrirPDFlink()
        else:
            conver.abrirPDF()
        
     
except IndexError as error:
    print(error)