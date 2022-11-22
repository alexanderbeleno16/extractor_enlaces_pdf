import pandas as pd 
import PyPDF2
import re

status = True 
try:
    
    # LINK_ARCHIVO_PDF = open(r'pdf_pruebas/ESTADO_1.pdf','rb') 
    LINK_ARCHIVO_PDF = open(r'pdf_pruebas/ESTADO_212.pdf','rb') 
    
    PDF = PyPDF2.PdfFileReader(LINK_ARCHIVO_PDF, strict=False)
    paginas = PDF.getNumPages()
    
    # print( paginas )
    # TodoContenidoTextoPdf = PDF.getPage().extract_text()
    # print( TodoContenidoTextoPdf )
    
    text=''
    for i in range(0,paginas):
        # creating a page object
        pageObj = PDF.getPage(i)
        # extracting text from page
        text=text+pageObj.extractText()
        print( pageObj.extract_text() )
    # print(text)
    
    

    # dominio = 'https://www.ramajudicial.gov.co'
    # key = '/Annots'
    # url = '/URI'
    # ank = '/A'
    
    key = '/Parent'
    url = '/FlateDecode'
    ank = '/Filter'
    mylist = []

    for page in range(paginas):
        paginaExtraida = PDF.getPage(page)
        ObjetoPaginaExtraida = paginaExtraida.getObject()
        
        # print(ObjetoPaginaExtraida)  
        # print(ObjetoPaginaExtraida.keys())  
        # print("------------------------------------------------")
        
        if key in ObjetoPaginaExtraida.keys():
            # print( ObjetoPaginaExtraida[key] )
            array_objetos = ObjetoPaginaExtraida[key]
            # array_objetos = ObjetoPaginaExtraida
            # print( array_objetos['/Kids'][0] ) 
            
            # for obj in array_objetos:
            #     try:
                    # objeto = obj.getObject()
                    # print( objeto[0] )
                    
                    # if url in objeto[ank].keys():
                        # print( objeto[ank][url] )
                    #     link=""
                    #     if ( re.search("^"+dominio+"*", objeto[ank][url]) ):
                    #         link = objeto[ank][url]
                    #     else:
                    #         link = dominio+str(objeto[ank][url])
                    #     mylist.append(link)
                    #     print(objeto[ank][url])
                # except KeyError:
                #     pass
                
                
                
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

