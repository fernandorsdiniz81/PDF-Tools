from pypdf import PdfReader, PdfWriter

class PdfTools:
    def merger(self, file_list, path):
        merger = PdfWriter()
                             
        for file in file_list:
            merger.append(file)

        merger.write(f"{path}/merged.pdf")
        merger.close()


    def compressor(self, path, file, file_name, compression, image_quality):
        level = compression
        quality = image_quality
        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        for page in writer.pages:
            page.compress_content_streams(level=level)
            for img in page.images:
                img.replace(img.image, quality=quality)

        with open(f"{path}/{file_name}", "wb") as f:
            writer.write(f)
