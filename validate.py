from PIL import Image
import os


verbose = False
summary = []
# loop over all sprites
for file in os.listdir("assets_mod/Sprite"):
    if file.endswith(".png"):
        print("Working on " + file)
        image = Image.open(os.path.join("assets_mod/Sprite", file))
        image_check = Image.open(os.path.join("assets_mod_check/Sprite", file))
        # check whether the images are exactly the same
        if image.size == image_check.size:
            width, height = image.size
            count = 0
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x, y))
                    pixel_original = image_check.getpixel((x, y))
                    if pixel != pixel_original and pixel[3] != 0:
                        if verbose:
                            print(
                                f"Error: Images not equal at ({x}, {y})",
                                image.getpixel((x, y)),
                                image_check.getpixel((x, y)),
                            )
                        count += 1
            if count == 0:
                print("Check: Sprite images are the same")
            else:
                print(f"Check: Sprite images are different by {count} pixels")
                summary.append(f"{file}: different by {count} pixels")
        else:
            print("Check: Sprite images have different sizes")
            summary.append(f"{file}: different sizes")
# print summary
print("-" * 80)
if summary:
    print("Summary: The following files are different:")
    for file in summary:
        print(file)
else:
    print("Summary: All files are the same")
