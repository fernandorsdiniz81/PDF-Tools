import interface
import PySimpleGUI as sg
import os
import webbrowser


class Application:
    def __init__(self) -> None:
        self.interface = interface.Interface() 


    def open_window(self):
        window = self.interface.create_window()
        file = ""
        file_list_string = ""
        file_list = []
        
        def show_merger_elements():
            window["merger_text"].update(visible=True)
            window["merger_listbox"].update(visible=True)
            window["limpar"].update(visible=True)
            window["deletar"].update(visible=True)
            window["up"].update(visible=True)
            window["down"].update(visible=True)
            window["mesclar"].update(visible=True)
        
        def hide_merger_elements():
            window["merger_listbox"].update(visible=False)
            window["merger_text"].update(visible=False)
            window["limpar"].update(visible=False)
            window["deletar"].update(visible=False)
            window["up"].update(visible=False)
            window["down"].update(visible=False)
            window["mesclar"].update(visible=False)
               
        def show_compressor_elements(): 
            window["compression_text"].update(visible=True)
            window["compression"].update(visible=True)
            window["image_quality_text"].update(visible=True)
            window["image_quality"].update(visible=True)
            window["compressor_text"].update(visible=True)
            window["compactar"].update(visible=True)
        
        def hide_compressor_elements():
            window["compression_text"].update(visible=False)
            window["compression"].update(visible=False)
            window["image_quality_text"].update(visible=False)
            window["image_quality"].update(visible=False)
            window["compactar"].update(visible=False)
            
        while True:
            event, value = window.read(timeout=100)
            #window['processing_animation'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)                                                  
            
            if event == sg.WIN_CLOSED:
                break
            
            ############ merger ####################################
            
            elif event == "arquivos": # para o merger
                file = sg.popup_get_file('Selecione os aquivos a serem mesclados', keep_on_top=True, file_types=((". pdf"),), multiple_files=True)
                
                if file != None and file != "":
                    file_list_string += f";{file}" # para não apensar ";" quando file for vazio
                
                file_list = file_list_string.split(";")
                
                try:
                    del file_list[0] # A lista terá sempre um elemento "" no índice 0
                except:
                    pass # Pois, quando o usuário cancela a seleção de arquivos, não é gerada uma lista
                
                # O método popup_get_file() quando seleciona múltiplos arquivos, retorna um objeto
                # do tipo lista, com 1 elemento, e separa os nomes dos arquivos com ";". Por isso
                # optei em retornar a relação de arquivos numa string e utilizar o método split(";")
                # para converter essa string em lista que possa ser utilizada corretamente. Tive que 
                # acrescentar ";" no início da string, pois o último arquivo não possui ";", logo, 
                # se o usuário fizer duas seleções, o último arquivo da primeira seleção 
                # não teria a separação ";" com o primeiro arquivo da segunda. Assim o primeiro item 
                # da string convertida em lista será vazio.
                
                if len(file_list) > 0:
                    window["merger_listbox"].update(file_list)
                    show_merger_elements()
                                               
            elif event == "limpar":
                file_list_string = ""
                file_list = []
                window["merger_listbox"].update("")
                hide_merger_elements()
            
            elif event == "deletar":
                try:
                    i = file_list.index(value["merger_listbox"][0])
                    del file_list[i]
                except:
                    if len(file_list) > 0:
                        del file_list[0]
                        if len(file_list) == 0:
                            hide_merger_elements()
                window["merger_listbox"].update(file_list)
                            
            elif event == "up":
                if value["merger_listbox"] != []:
                    i = file_list.index(f'{value["merger_listbox"][0]}')
                    if i > 0:
                        item = file_list.pop(i)
                        file_list.insert(i-1, item)
                    window["merger_listbox"].update(file_list)
                                    
            elif event == "down":
                if value["merger_listbox"] != []:
                    i = file_list.index(f'{value["merger_listbox"][0]}')
                    if i <= len(file_list)-1:
                        item = file_list.pop(i)
                        file_list.insert(i+1, item)
                    window["merger_listbox"].update(file_list)

            elif event == "mesclar":
                if len(file_list) > 1:
                    path = sg.popup_get_folder('Selecione onde o arquivo "merged.pdf" será salvo:', keep_on_top=True)
                    if path != None:
                        self.interface.run_merger(file_list, path)
                        if os.path.exists(f"{path}/merged.pdf"):
                            hide_merger_elements()
                            sg.popup("Pronto!", )
                        else:
                            sg.popup("Erro ao salvar o arquivo!", )
                    else:
                        sg.popup('Escolha onde será salvo o arquivo "merged.pdf"!', )
                else:
                    sg.popup("Selecione pelo menos 2 arquivos!", )
            
            ############ compressor ####################################
            
            elif event == "arquivo": # para o compressor
                file_to_compress = sg.popup_get_file('Selecione um arquivo a ser compactado', keep_on_top=True, file_types=((". pdf"),))
                if file_to_compress != None:
                    show_compressor_elements()
                                
            elif event == "compactar":
                compression = value["compression"]
                image_quality = value["image_quality"]
                file_name = f"{self.interface.simplify_file_name(file_to_compress[:-4])}-compressed.pdf"
                path = sg.popup_get_folder(f'Selecione onde o arquivo "{file_name}" será salvo:', keep_on_top=True)
                compressed_file = f"{path}/{file_name}"
                
                if path != None:
                    initial_size = os.path.getsize(file_to_compress)
                    #window["processing_animation"].update(visible=True)
                    self.interface.run_compressor(path, file_to_compress, file_name, compression, image_quality)
                    
                    if os.path.exists(compressed_file):
                        hide_compressor_elements()
                        #window["processing_animation"].update(visible=False)
                        final_size = os.path.getsize(compressed_file)
                        size_delta = round((final_size / initial_size)*100)
                        
                        if size_delta < 100: # Alguns arquivos já são otimizados e não permitem compressão, podendo até mesmo aumentar de tamanho
                            sg.popup(f"Pronto!\nO arquivo compactado tem {size_delta}% do tamanho do arquivo original.", )
                        else:
                            os.remove(compressed_file)
                            sg.popup(f"O arquivo {file_to_compress} já é altamente otimizado e não permite compressão.", )
                    
                    else:
                        hide_compressor_elements()
                        #window["processing_animation"].update(visible=False)
                        sg.popup("Erro ao salvar o arquivo!", )
               
                else:
                    sg.popup(f'Você tem que escolher onde será salvo o arquivo "{file_name}"!', )

            ############ menu ##########################################
                   
            elif event == "sobre":
                sg.popup(self.interface.about, title="Sobre esta aplicação")
            
            elif event == "contato":
                sg.popup(self.interface.contact, title="Contato")

            elif event == "código fonte":
                webbrowser.open(self.interface.git)
                        
        window.close()



if __name__ == "__main__":
    app = Application()
    app.open_window()