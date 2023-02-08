import argparse
import uuid

import segno
from PIL import Image, ImageFont, ImageDraw


class AddInventory:
    URL_PREFIX = "https://mcquaidrobotics.github.io"
    EDIT_URL_PREFIX = "https://github.com/McQuaidRobotics/inv/blob/main"
    TITLE_FONT = ImageFont.truetype("assets/arial.ttf", 110)
    SMALLER_FONT = ImageFont.truetype("assets/arial.ttf", 70)
    SMALLEST_FONT = ImageFont.truetype("assets/arial.ttf", 50)
    LARGER_FONT = ImageFont.truetype("assets/arial.ttf", 200)
    LARGEST_FONT = ImageFont.truetype("assets/arial.ttf", 600)

    def __init__(
        self,
        product: str,
        quantity: int,
        year: int,
        name: str = None,
        canid: int = None,
        debug: bool = False
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.year = year
        self.name = name
        self.canid = canid
        self.debug = debug

        for i in range(self.quantity):
            self.create_qr_and_md_files()

    def create_qr_and_md_files(self) -> None:
        # Generate Guid
        guid = uuid.uuid4()
        # Create QR Code
        qr_data = f"{self.URL_PREFIX}/inv/guids/{guid}"
        QRcode = segno.make(qr_data, error="H", micro=False)
        if self.debug:
            qr_pafn = "images/qrcode.png"
        else:
            qr_pafn = f"images/{guid}.png"
        QRcode.save(qr_pafn, scale=8)
        # Create label for printing (use default label template)
        label_img = Image.open("assets/LabelTemplate.png")
        # Add QR Code to label
        qr_img = Image.open(qr_pafn)
        label_img.paste(qr_img, (120, 1000))
        # Add year to label
        year_img = Image.new("RGBA", (255, 125), (255, 255, 255, 255))
        year_draw = ImageDraw.Draw(year_img)
        year_draw.text(
            xy=(0, 0),
            text=str(self.year),
            font=self.TITLE_FONT,
            fill="black"
        )
        year_img = year_img.rotate(-90, expand=True)
        label_img.paste(year_img, (695, 1150), year_img)
        # Add product to label
        product_img = Image.new("RGBA", (500, 45), (255, 255, 255, 255))
        product_draw = ImageDraw.Draw(product_img)
        product_draw.text(
            xy=(0, 0),
            text=str(self.product),
            font=self.SMALLEST_FONT,
            fill="black"
        )
        product_img = product_img.rotate(-90, expand=True)
        label_img.paste(product_img, (38, 300))
        # Add guid to label
        guid_img = Image.new("RGBA", (315, 65), (255, 255, 255, 255))
        guid_draw = ImageDraw.Draw(guid_img)
        guid_draw.text(
            xy=(0, 0),
            text=f'{guid}'[0:8],
            font=self.SMALLER_FONT,
            fill="black"
        )
        guid_img = guid_img.rotate(-90, expand=True)
        label_img.paste(guid_img, (585, 1050))
        if self.canid:
            # Add CANID to label
            canid_h = 650
            canid_w = 500
            canid_img = Image.new(
                "RGBA",
                (canid_h, canid_w),
                (255, 255, 255, 255)
            )
            canid_draw = ImageDraw.Draw(canid_img)
            canid_draw.text(
                xy=(canid_h // 2, canid_w // 2),
                text=str(self.canid),
                font=self.LARGEST_FONT,
                anchor="mm",
                fill="black"
            )
            canid_img = canid_img.rotate(-90, expand=True)
            label_img.paste(canid_img, (75, 220))
        elif self.name:
            # Add name to label
            name_h = 850
            name_w = 300
            name_img = Image.new(
                "RGBA",
                (name_h, name_w),
                (255, 255, 255, 255)
            )
            name_draw = ImageDraw.Draw(name_img)
            name_draw.text(
                xy=(name_h // 2, name_w // 2),
                text=str(self.name),
                font=self.LARGER_FONT,
                anchor="ms",
                fill="black"
            )
            name_img = name_img.rotate(-90, expand=True)
            label_img.paste(name_img, (100, 95))

        # Save label
        if self.debug:
            label_img.save("images/label_dev.png")
        else:
            label_img.save(f"images/labels/lb-{guid}.png")
        # Create markdown file
        file_text = f"# **{self.year} {self.product}**"
        if self.name:
            file_text += f" - **{self.name}**"
        file_text += "\n---\n\n"
        file_text += f"![{guid}]({self.URL_PREFIX}/inv/images/{guid}.png)\n\n"
        file_text += (
            f"[{guid}]({self.URL_PREFIX}/inv/images/labels/lb-{guid}.png)\n\n"
        )
        file_text += "Serial Number: \n\n"
        file_text += "Connectorized: \n\n"
        file_text += "Tested: \n\n"
        file_text += "Used In: \n\n\n"
        file_text += (
            '###### [<div style="text-align: right"><sub>'
            'Edit'  # Text for the link to edit the page
            '</sub></div>]'
            f'({self.EDIT_URL_PREFIX}/guids/{guid}.md)\n\n'
        )
        print(f'Created {guid}.md and {guid}.png')
        if self.debug:
            with open("guids/markdown_dev.md", "w") as f:
                f.write(file_text)
        else:
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
    parser.add_argument(
        "-n",
        "--name",
        help="Text added to label Box",
        required=False
    )
    parser.add_argument(
        "-c",
        "--canid",
        help="CAN ID of device",
        type=int,
        required=False
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="CAN ID of device",
        type=bool,
        default=False
    )
    args = parser.parse_args()
    AddInventory(
        product=args.product,
        quantity=args.quantity,
        year=args.year,
        name=args.name,
        canid=args.canid,
        debug=args.debug)
