import pandas as pd 
import PyPDF2
import re



def extraerEnlaces(PDF):
    mylistEnlace = []
    dominio = 'http://visordocs.sic.gov.co:8080/'
    key = '/Annots'
    url = '/URI'
    ank = '/A'    
    
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


def extraerRadicados(PDF):
    mylistRadicado = []  
    
    for page in range(paginas):
        paginaExtraida = PDF.getPage(page)
        
        texto = paginaExtraida.extractText() #TODO EL TEXTO POR PAGINAS
        texto = str(texto).replace('\\','')
        texto = re.findall(r"([0-9][0-9][-][0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?)", texto) #<List>RADICADO ANIO Y RADICADO SEPARADO POR GUIONES. EJ: 22-426253 
                
        print( "\n\n <<<<<<<<< Hoja # ---> {} >>>>>>>>>>\n".format(page+1) , "Radicados: ", texto )
        
    # return mylistRadicado




status = True 
mylist = []
content = {}
try:
    LINK_ARCHIVO_PDF = open(r'pdf_pruebas/ESTADO_212.pdf','rb')
    
    PDF = PyPDF2.PdfFileReader(LINK_ARCHIVO_PDF, strict=False)
    paginas = PDF.getNumPages()

    mylistRadicado = extraerRadicados(PDF)
    mylistEnlace = extraerEnlaces(PDF)
    
    # for radicado in mylistRadicado:
    #     print( radicado )
             
    # print( mylistEnlace )
    # exit()
        
    
        
 
    print("\n\nPagina(s) encontrada(s): {}".format(paginas))            
    print("Links encontrado(s): {}".format(len(mylistEnlace)))   
except FileNotFoundError as error:
    status = False 
    