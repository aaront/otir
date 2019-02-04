import io
import click
import requests
from PIL import Image


def get_image(image_url: str) -> Image:
    r = requests.get(image_url)
    if r.status_code == 200:
        return Image.open(io.BytesIO(r.content))


def resize_image(image: Image, width: int) -> Image:
    image_width = image.size[0]
    image_height = image.size[1]
    width = min([width, image_width])
    width_percent = (width/float(image_width))
    height = int(float(image_height)*float(width_percent))
    return image.resize((width, height), Image.LANCZOS)


def crop_image(image: Image, width: int) -> Image:
    scale = 3
    image_width = image.size[0]
    image_height = image.size[1]
    height = min([width, image_width]) / scale
    if height > image_height:
        height_diff = height - image_height
        crop_width = (height_diff * scale) / 2
        return image.crop((crop_width, 0, image_width-crop_width, image_height))
    crop_height = (image_height - height) / 2
    return image.crop((0, crop_height, image_width, image_height-crop_height))


@click.command()
@click.argument('url')
@click.option('--width', '-w', default=1000, show_default=True, type=int)
def main(url: str, width: int):
    file_name = url.split('/')[-1]
    click.echo(f'Downloading and resizing \'{file_name}\'')
    image = get_image(url)
    image = resize_image(image, width)
    image = crop_image(image, width)
    image.save(file_name)

if __name__ == '__main__':
    main()