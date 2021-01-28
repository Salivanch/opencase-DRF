
from django.template.defaultfilters import slugify as django_slugify
from PIL import Image

def resize_photo(path):
    image = Image.open(path)
    if image.height > 256 or image.width > 256:
        resize = (256, 256)
        image.thumbnail(resize)
        image.save(path)
        return image


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'
}

def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))
