import math
from PIL import Image

class CoordinateIterator:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.current_coord = (0, 0)
    
    def has_next(self) -> bool:
        return 0 <= self.current_coord[0] < self.size[0] and 0 <= self.current_coord[1] < self.size[1]
    
    def next(self) -> tuple[int, int]:
        if self.has_next():
            tmp = self.current_coord
            x, y = self.current_coord
            x += 1
            if x >= self.size[0]:
                x = 0
                y += 1
            self.current_coord = (x, y)
            return tmp
        else:
            raise IndexError('End of grid reached.')
    
    def reset(self) -> None:
        self.current_coord = (0, 0)

class ImageBuilder:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.iterator = CoordinateIterator(self.size)
        self.img = Image.new("L", self.size)
    
    def write(self, data: bytes) -> None:
        for byte in data:
            coord = self.iterator.next()
            self.img.putpixel(coord, byte)
    
    def build(self) -> Image.Image:
        tmp = self.img
        self.reset()
        return tmp
    
    def reset(self) -> None:
        self.img = Image.new("L", self.size)
        self.iterator.reset()
    
    def has_next(self) -> bool:
        return self.iterator.has_next()

class ImageReader:
    def __init__(self, path_or_img) -> None:
        if isinstance(path_or_img, str):
            self.img = Image.open(path_or_img)
        else:
            self.img = path_or_img
        self.iterator = CoordinateIterator(self.img.size)
        self.pixels = self.img.load()
    
    def read_pixel(self):
        x, y = self.iterator.next()
        return bytes([self.pixels[x, y]])

    def has_next(self) -> bool:
        return self.iterator.has_next()

class ImageManager:
    def __init__(self, size: tuple[int, int], savepath: str) -> None:
        self.size = size
        self.savepath = savepath
        self.img_builder = ImageBuilder(size)
        self.count = 0
    
    def write(self, data: bytes) -> None:
        if not self.img_builder.has_next():
            self.save_and_reset()
        self.img_builder.write(data)
    
    def save_and_reset(self):
        img = self.img_builder.build()
        img.save(f'{self.savepath}/{self.count}.png')
        self.count += 1