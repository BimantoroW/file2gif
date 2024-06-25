from imageutils import ImageReader
from PIL import Image

class Decoder:
    def decode(self, path: str) -> None:
        gif = Image.open(path)
        img_reader = ImageReader(gif.copy().convert("L"))
        filename, filesize = self._read_header(img_reader)

        read_bytes = 0
        with open(filename, 'wb') as f:
            while read_bytes < filesize:
                if not img_reader.has_next():
                    gif.seek(gif.tell() + 1)
                    img_reader = ImageReader(gif.copy().convert("L"))
                f.write(img_reader.read_pixel())
                read_bytes += 1

    def _read_header(self, img_reader: ImageReader) -> None:
        len_filename = img_reader.read_pixel() + img_reader.read_pixel()
        len_filename = int.from_bytes(len_filename, 'big')
        filename = ""
        for i in range(len_filename):
            filename += img_reader.read_pixel().decode()
        
        filesize = bytes()
        for i in range(8):
            filesize += img_reader.read_pixel()
        filesize = int.from_bytes(filesize, 'big')

        return filename, filesize