from numpy import extract
import pandas as pd 
import PyPDF2
import re
import sys

class Extractor_Enlaces:
    def __init__(self, ruta_archivo):
        #------------RUTA DEL ARCHIVO--------------
        self.archivo  = ruta_archivo
    
    def extraer_enlaces(self):
        try:
            status = True             
            LINK_ARCHIVO_PDF = open(str(self.archivo),'rb')   #OK
            
            PDF = PyPDF2.PdfFileReader(LINK_ARCHIVO_PDF, strict=False)
            paginas = PDF.getNumPages()

            #RAMA
            dominio = 'https://www.ramajudicial.gov.co'
            dominio2 = 'http://www.ramajudicial.gov.co'
            path_rama = '/documents'
            
            #SAMAI
            dominio_samai = 'https://samairj.consejodeestado.gov.co'
            path_samai    = '/Vistas/documentos/downloader.aspx'
            
            #SharePoint
            #NOTA: Los enlaces "SharePoint" no tienen el año y rad en la url.
            # dominio3 = 'https://etbcsj-my.sharepoint.com/'
            # or re.search("^"+dominio3+"*", objeto[ank][url])
            
            key = '/Annots'
            url = '/URI'
            ank = '/A'
            mylist = []

            for page in range(paginas):
                paginaExtraida = PDF.getPage(page)
                ObjetoPaginaExtraida = paginaExtraida.getObject()
                # print(ObjetoPaginaExtraida.keys())  
                if key in ObjetoPaginaExtraida.keys():
                    array_objetos = ObjetoPaginaExtraida[key]
                    for obj in array_objetos:
                        try:
                            objeto = obj.getObject()
                            # print( objeto[ank].keys() )
                            if url in objeto[ank].keys():
                                link=""
                                if ( re.search("^"+dominio+path_rama+"*", objeto[ank][url]) or re.search("^"+dominio2+path_rama+"*", objeto[ank][url]) or re.search("^"+dominio_samai+path_samai+"*", objeto[ank][url]) ): 
                                    link = objeto[ank][url]
                                else:
                                    if( re.search("^"+path_rama+"*", objeto[ank][url]) ):
                                        link = dominio+str(objeto[ank][url])
                                
                                if (link!=""):
                                    mylist.append(link)                                    
                                # print(objeto[ank][url])
                        except KeyError:
                            pass
                       
            # print("Pagina(s) encontrada(s): {}".format(paginas))            
            sin_duplicados = set(mylist)
            new_list = list(sin_duplicados)
            # print("Links encontrado(s): {}".format(len(new_list)))            
            # print( new_list )  #IMPRIME LA LISTA DE LOS LINKS PDF
            enlaces_concatenados=""
            if (len(new_list)>0):
                for enlace in new_list:
                    enlaces_concatenados += str(enlace)+"||" #+"\n"
            enlaces_concatenados+="Cantidad enlaces: {}".format(len(new_list))
            
        except FileNotFoundError as error:
            status = False 
         
        if status:
            return(enlaces_concatenados) #Se hace print de los enlaces concatenados el cual recibirá PHP para hacerle el explode separados por ||
        else:
            return("Archivo_no_encontrado")       


try:
    if(sys.argv[1] == ''):
        raise IndexError('Nombre del archivo vacio (CONSOLA: EXTRACTOR DE ENLACES)')
        
    file_name = sys.argv[1]
    # INSTANCIA DE LA CLASE EXTRACTOR DE ENLACES:
    obj_extract = Extractor_Enlaces(file_name)
    respuesta = obj_extract.extraer_enlaces()
    print( respuesta )
    
except IndexError:
        print('Archivo_no_encontrado_(1)')

