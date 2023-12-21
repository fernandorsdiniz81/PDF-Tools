import PySimpleGUI as sg
import pdftools
import re

class Interface:
    def __init__(self):
        self.favorites_themes = "SystemDefault SystemDefaultForReal SystemDefault1 LightBrown12 DarkGrey10 LightGreen4 Reddit DarkTeal11 DarkGrey7 DarkBlue LightBrown12".split()
        self.pdf_tools = pdftools.PdfTools()
    

    def simplify_file_name(self, file): # para excluir o path do nome do arquivo
        pattern = re.compile(r"(.*/)*")
        complete_path = file
        test = re.match(pattern, complete_path)
        if test:
            partial_path = test.group(0)
            file = complete_path.replace(partial_path, "")
        return file
            
        
    def run_merger(self, file_list, path):
        self.pdf_tools.merger(file_list, path)
        
    
    def run_compressor(self, path, file, file_name, compression, image_quality):
        self.pdf_tools.compressor(path, file, file_name, compression, image_quality)
        
    
    def create_window(self):
        sg.theme("SystemDefaultForReal")
        menu = [["&menu",["&sobre", "&contato", "código &fonte"]]]
        self.about = "Esta é uma aplicação independente, com a finalidade de facilitar a manipulação de arquivos PDF.\n\nEm nenhum momento os arquivos são compartilhados na internet.\n"
        self.contact = "Fernando Diniz\ne-mail: fernandorsdiniz@gmail.com\nWhatsapp/Telegram: (31)98777-2280"
        self.git = "https://github.com/fernandorsdiniz81/PDF-Tools/"
       
        merger_layout = [
                [sg.Text("Selecione os arquivos a serem mesclados:")],
                [sg.Button("arquivos")],
                [sg.ProgressBar(100, orientation='h', size=(30, 30), key='progress_bar', visible=False)],
                [sg.Text("Aquivos a serem mesclados (nesta ordem):", key="merger_text", visible=False, size=(350,1))],
                [sg.Listbox([], key="merger_listbox", expand_x=True, expand_y=True, horizontal_scroll=True, visible=False)],
                [sg.Button("limpar", visible=False), sg.Button("deletar", visible=False), sg.Button("↑", key="up", visible=False), sg.Button("↓", key="down", visible=False), sg.Button("mesclar", bind_return_key=True, visible=False)]
                ]
        
        compressor_layout = [
                [sg.Text("Selecione o arquivo a ser compactado:")],
                [sg.Button("arquivo")],
                [sg.Text("nível de compressão: ", key="compression_text", visible=False), sg.Spin([i for i in range(1,10)], initial_value=9, key='compression', size=(3,1), visible=False)],
                [sg.Text("qualidade das imagens:", key="image_quality_text", visible=False), sg.Spin([i for i in range(1,101)], initial_value=80, key='image_quality', size=(3,1), visible=False)],
                [sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='processing_animation', visible=False)],
                [sg.Text("O tamanho do arquivo compactado varia em \nrazão da otimização do arquivo original.", key="compressor_text", visible=False, size=(350,2))],
                [sg.Button("compactar", bind_return_key=True, visible=False)]
                ]
        
        layout = [[sg.Menu(menu, key="menu")],
                [sg.TabGroup([[ sg.Tab("mesclagem", merger_layout), 
                                sg.Tab("compactação", compressor_layout)]], key="tabs", expand_x=True, expand_y=True, selected_background_color="lightblue")]
                ]   
        
        window = sg.Window("PDF Tools", layout, size=(350,400))
        return window