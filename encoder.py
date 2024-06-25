import os, glob, contextlib
from PIL import Image
from imageutils import ImageManager, ImageBuilder

class Encoder:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.img_manager = ImageManager(size, 'tmp')
        self.img_builder = ImageBuilder(size)
    
    def encode(self, path: str) -> None:
        self._encode_to_pngs(path)
        
        # filepaths
        filename = path.split('/')[-1]
        filename, extension = filename.split('.')
        fp_in = "tmp/*.png"
        fp_out = f"out/{filename}.gif"

        # use exit stack to automatically close opened images
        with contextlib.ExitStack() as stack:

            # lazily load images
            imgs = (stack.enter_context(Image.open(f))
                    for f in sorted(glob.glob(fp_in)))

            # extract  first image from iterator
            img = next(imgs)

            # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
            img.save(fp=fp_out, format='GIF', append_images=imgs,
                    save_all=True, duration=200, loop=0)
        
        self._delete_tmp()
    
    def _encode_to_pngs(self, path: str) -> None:
        with open(path, 'rb') as f:
            self._add_header(path)
            while byte := f.read(1):
                self.img_manager.write(byte)
            self.img_manager.save_and_reset()
    
    def _add_header(self, path: str) -> None:
        filename = path.split('/')[-1]
        len_filename = len(filename).to_bytes(2, 'big')
        self.img_manager.write(len_filename)
        self.img_manager.write(filename.encode())

        filesize = os.path.getsize(path).to_bytes(8, 'big')
        self.img_manager.write(filesize)
    
    def _delete_tmp(self):
        for root, dirs, files in os.walk('tmp'):
            for f in files:
                os.remove(os.path.join(root, f))