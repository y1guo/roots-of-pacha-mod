from PIL import Image
import os


def get_texture_size(path: str):
    width, height = 0, 0
    with open(path) as f:
        lines = f.read().splitlines()
        for line in lines:
            if "int m_Width = " in line:
                width = int(line.split("int m_Width = ")[1])
            if "int m_Height = " in line:
                height = int(line.split("int m_Height = ")[1])
    return width, height


def get_sprite_size(path: str):
    x, y, width, height = 0, 0, 0, 0
    with open(path) as f:
        lines = f.read().splitlines()
        flag = -1
        for line in lines:
            if flag == 4:
                break
            if "Rectf m_Rect" in line:
                flag = 0
                continue
            if flag != -1 and "float x = " in line:
                x = int(line.split("float x = ")[1])
                flag += 1
            if flag != -1 and "float y = " in line:
                y = int(line.split("float y = ")[1])
                flag += 1
            if flag != -1 and "float width = " in line:
                width = int(line.split("float width = ")[1])
                flag += 1
            if flag != -1 and "float height = " in line:
                height = int(line.split("float height = ")[1])
                flag += 1
    return x, y, width, height


def compare_to_original(name: str):
    # load the texture images
    image = Image.open(os.path.join("assets_mod/Texture2D", name + "_Portraits.png"))
    image_original = Image.open(os.path.join("assets/Texture2D", name + "_Portraits.png"))
    # get the texture size
    assert image.size == image_original.size
    width, height = image.size
    # compare the original texture image with the new texture image
    count = 0
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            pixel_original = image_original.getpixel((x, y))
            if pixel != pixel_original and pixel[3] != 0:
                if verbose:
                    print(
                        "Error: texture image not equal at ({}, {})".format(x, y),
                        image.getpixel((x, y)),
                        image_original.getpixel((x, y)),
                    )
                count += 1
    if count == 0:
        print("TEST: Texture image is the same as original")
    else:
        print("TEST: Texture image is {} pixels different from the original".format(count))


# control the verbosity
verbose = False
# loop over all textures
for texture_dump in os.listdir("dumps/Texture2D"):
    if texture_dump.endswith("_Portraits.txt"):
        name = texture_dump.split("_Portraits.txt")[0]
        print("Working on" + name)
    else:
        continue
    # get the texture size
    texture_width, texture_height = get_texture_size(os.path.join("dumps/Texture2D", texture_dump))
    if verbose:
        print("Width: {}, Height: {}".format(texture_width, texture_height))
    # create new texture image
    texture_image = Image.new("RGBA", (texture_width, texture_height))
    # loop over all sprites
    for sprite_dump in os.listdir("dumps/Sprite"):
        if sprite_dump.startswith(name):
            sprite_name = sprite_dump.split(".txt")[0]
            # get the sprite size
            sprite_x, sprite_y, sprite_width, sprite_height = get_sprite_size(
                os.path.join("dumps/Sprite", sprite_dump)
            )
            # fix sprite_y by counting from the upper left corner
            sprite_y = texture_height - sprite_y - sprite_height
            if verbose:
                print(
                    "{:>4d}{:>4d}{:>4d}{:>4d}".format(sprite_x, sprite_y, sprite_width, sprite_height),
                    sprite_name,
                )
            # load the sprite image
            sprite_image = Image.open(os.path.join("assets_mod/Sprite", sprite_name + ".png"))
            # check that the size of the sprite image is correct
            assert sprite_image.size == (sprite_width, sprite_height)
            # paste the sprite image into the texture image
            box = (sprite_x, sprite_y, sprite_x + sprite_width, sprite_y + sprite_height)
            texture_image.paste(sprite_image, box)
    # save the texture image
    texture_image.save(os.path.join("assets_mod/Texture2D", name + "_Portraits.png"))
    # test
    compare_to_original(name)
