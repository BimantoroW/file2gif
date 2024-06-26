import os, shutil
from PIL import Image
from imageutils import ImageManager, ImageBuilder

MAX_IMGS = 20

class Encoder:
    def __init__(self, path: str, size: tuple[int, int]) -> None:
        self.path = path
        filename_extension = path.split('/')[-1].split('.')
        self.filename = filename_extension[0]
        if len(filename_extension) > 1:
            self.extension = '.' + filename_extension[1]
        else:
            self.extension = ''

        self.size = size
        self.img_manager = ImageManager(size, MAX_IMGS, self._on_manager_full)
    
    def encode(self) -> None:
        if not os.path.isdir('out'):
            os.mkdir('out')
        if os.path.isfile(f'out/{self.filename}.gif'):
            os.remove(f'out/{self.filename}.gif')

        with open(self.path, 'rb') as f:
            self._add_header()
            while byte := f.read(1):
                self.img_manager.write(byte)
            self.img_manager.save_and_reset(True)
    
    def _add_header(self) -> None:
        filename_extension = self.filename + self.extension
        len_filename = len(filename_extension).to_bytes(2, 'big')
        self.img_manager.write(len_filename)
        self.img_manager.write(filename_extension.encode())

        filesize = os.path.getsize(self.path).to_bytes(8, 'big')
        self.img_manager.write(filesize)
    
    def _on_manager_full(self, imgs: list[Image.Image]) -> None:
        path = f'out/{self.filename}.gif'

        if os.path.isfile(path):
            with Image.open(path) as existing_gif:
                existing_gif.save('out/tmp.gif', save_all=True, append_images=imgs, loop=0, duration=200)
            shutil.move('out/tmp.gif', path)
        else:
            imgs[0].save(path, save_all=True, append_images=imgs[1:], loop=0, duration=200)