import pandas as pd 
import PyPDF2
import re

status = True 
try:
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/060 OOHH.pdf','rb')   #OK
    LINK_ARCHIVO_PDF = open(r'pdf_pruebas/documentos_prueba_autos_sr_juan/PRUEBA_1.pdf','rb') #OK
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/Estado Electronico No. 065F.pdf','rb')    #OK
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/Estado No. 114.pdf','rb') #REGULAR {DOMINIO}
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/ESTADO_1.pdf','rb')   #OK
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/Estado20220726N083.pdf','rb') #REGULAR {DOMINIO}
    # LINK_ARCHIVO_PDF = open(r'carpeta_pdf/documentos_prueba_autos_sr_juan/pequeñas causas - laboral 004 barranquilla_27-07-2022 RAMA.pdf','rb') #OK
    
    PDF = PyPDF2.PdfFileReader(LINK_ARCHIVO_PDF, strict=False)
    paginas = PDF.getNumPages()

    dominio = 'https://www.ramajudicial.gov.co'
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
                        if ( re.search("^"+dominio+"*", objeto[ank][url]) ):
                            link = objeto[ank][url]
                        else:
                            link = dominio+str(objeto[ank][url])
                        mylist.append(link)
                        # print(objeto[ank][url])
                except KeyError:
                    pass
                
                
                
    print("Pagina(s) encontrada(s): {}".format(paginas))            
    sin_duplicados = set(mylist)
    new_list = list(sin_duplicados)
    print("Links encontrado(s): {}".format(len(new_list)))            
    # print( new_list )  #IMPRIME LA LISTA DE LOS LINKS PDF, ESTA COMENTADO PORQUE NECESITO UN STRING SEPARADOS POR || PARA HACERLE UN EXPLODE EN PHP




    enlaces_concatenados=""
    if (len(new_list)>0):
        for enlace in new_list:
            enlaces_concatenados += str(enlace)+"||"
    str(enlaces_concatenados)+"Cantidad enlaces: {}".format(len(new_list))
    
except FileNotFoundError as error:
    status = False 
    

if status:
    print(enlaces_concatenados) #Se hace print de los enlaces concatenados el cual recibirá PHP para hacerle el explode separados por ||
else:
    print("Archivo_no_encontrado")

