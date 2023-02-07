import argparse
import uuid

import segno
from PIL import Image, ImageFont, ImageDraw


class add_inventory:
    URL_PREFIX = "https://mcquaidrobotics.github.io"

    def __init__(self, product, quantity, year):
        self.product = product
        self.quantity = quantity
        self.year = year
        self.title_font = ImageFont.truetype("assets/arial.ttf", 110)
        self.guid_font = ImageFont.truetype("assets/arial.ttf", 50)

        for i in range(self.quantity):
            self.create_qr_and_md_files()

    def create_qr_and_md_files(self):
        # Generate Guid
        guid = uuid.uuid4()
        # Create QR Code
        qr_data = f"{self.URL_PREFIX}/inv/guids/{guid}"
        QRcode = segno.make(qr_data, error="H", micro=False)
        QRcode.save(f"images/{guid}.png", scale=8)
        # Create label for printing (use default label template)
        label_img = Image.open("assets/LabelTemplate.png")
        # Add QR Code to label
        qr_img = Image.open(f"images/{guid}.png")
        label_img.paste(qr_img, (120, 1000))
        # Add year to label
        year_img = Image.new("RGBA", (255, 125), (255, 255, 255, 255))
        year_draw = ImageDraw.Draw(year_img)
        year_draw.text(
            xy=(0, 0),
            text=str(self.year),
            font=self.title_font,
            fill="black"
        )
        year_img = year_img.rotate(-90, expand=True)
        label_img.paste(year_img, (695, 1150), year_img)
        # Add guid to label
        guid_img = Image.new("RGBA", (225, 55), (255, 255, 255, 255))
        guid_draw = ImageDraw.Draw(guid_img)
        guid_draw.text(
            xy=(0, 0),
            text=f'{guid}'[0:8],
            font=self.guid_font,
            fill="black"
        )
        guid_img = guid_img.rotate(-90, expand=True)
        label_img.paste(guid_img, (595, 1135), guid_img)
        # Save label
        label_img.save(f"images/labels/lb-{guid}.png")
        # Create markdown file
        file_text = f"# **{self.year} {self.product}**\n---\n\n"
        file_text += f"![{guid}]({self.URL_PREFIX}/inv/images/{guid}.png)\n\n"
        file_text += "Serial Number: \n\n"
        file_text += "Connectorized: \n\n"
        file_text += "Tested: \n\n"
        file_text += "Used In: \n\n"
        print(f'Created {guid}.md and {guid}.png')
        with open(f"guids/{guid}.md", "w") as f:
            f.write(file_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--product",
        help="Product name",
        required=True
    )
    parser.add_argument(
        "-q",
        "--quantity",
        help="Number of items to add",
        type=int,
        required=True
    )
    parser.add_argument(
        "-y",
        "--year",
        help="Year of product",
        type=int,
        required=True
    )
    args = parser.parse_args()
    add_inventory(args.product, args.quantity, args.year)
