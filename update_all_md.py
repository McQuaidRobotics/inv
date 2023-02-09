import os

from create_guid_file import AddInventory


class UpdateAllMd:
    def __init__(self, path="guids", debug=True):
        self.path = path
        self.debug = debug
        self.files = os.listdir(self.path)

        self.update()

    def update(self):
        for file in self.files:
            if file.endswith(".md"):
                guid = file.replace(".md", "")
                updated = False
                with open(f'{self.path}/{file}', "r") as f:
                    lines = f.readlines()
                    # Add label link if not already present
                    if not lines[5].startswith('['):
                        lines.insert(4, '\n')
                        lines.insert(
                            5,
                            f'[{guid}]'
                            f'({AddInventory.URL_PREFIX}'
                            f'/inv/images/labels/lb-{guid}.png)'
                        )
                        lines.insert(6, '\n')
                        lines.append('\n')
                        updated = True
                    else:
                        pass
                    # Add edit link if not already present
                    if not lines[-3].startswith('######'):
                        lines.append(
                            '###### [<div style="text-align: right"><sub>'
                            'Edit'  # Text displayed to edit link
                            '</sub></div>]'
                            f'({AddInventory.EDIT_URL_PREFIX}/guids/{guid}.md)'
                        )
                        lines.append('\n')
                        lines.append('\n')
                        updated = True
                    else:
                        pass

                if updated:
                    if self.debug:
                        output = f'{self.path}/dev.md'
                        print(f"Overwriting {guid} into {output}")
                    else:
                        print(f"Updating {file}")
                        output = f'{self.path}/{file}'
                with open(output, "w") as f:
                    f.writelines(lines)


if __name__ == "__main__":
    update_all_md = UpdateAllMd(debug=False)
