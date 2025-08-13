from PIL import Image, ImageFont, ImageDraw


class Margin:
    """
    Margin settings class.
    """

    def __init__(self, top=0, bottom=0, right=0, left=0):
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left


class Padding:
    """
    Cell padding settings class.
    """

    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height


class Colors:
    """
    Color settings class.
    """

    def __init__(
        self,
        bg=0,
        cell_bg="white",
        header_bg="gray",
        font="black",
        row_line="black",
        col_line="black",
        red="red",
        green="green",
    ):
        self.bg = bg
        self.cell_bg = cell_bg
        self.header_bg = header_bg
        self.font = font
        self.row_line = row_line
        self.col_line = col_line
        self.red = red
        self.green = green


class TableImage:
    """
    Image of table.
    """

    def __init__(
        self,
        table: list[list[str]],
        font=ImageFont.load_default(),
        cell_pad=Padding(),
        margin=Margin(),
        colors=Colors(),
        stock=False,
    ):
        """
        Create a table image.

        :param table:    A 2D list of strings.
        :param font:     An ImageFont object.
        :param cell_pad: Padding for cell, (top_bottom, left_right).
        :param margin:   Margin for table, (top, bottom, left, right).
        :param colors:   Color settings.
        :param stock:    Boolean, set red/green font color for cells start with +/-.
        """
        self.table = table.copy()
        self.font = font
        self.cell_pad = cell_pad
        self.margin = margin
        self.colors = colors
        self.stock = stock

        # compute dimensions
        self.row_height = [0] * len(self.table)
        self.col_width = [0] * len(max(self.table, key=len))
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                (width, height) = self.text_size(cell)
                self.col_width[j] = max(width, self.col_width[j])
                self.row_height[i] = max(height, self.row_height[i])
        self.tab_width = (
            sum(self.col_width) + len(self.col_width) * 2 * self.cell_pad.width
        )
        self.tab_height = (
            sum(self.row_height) + len(self.row_height) * 2 * self.cell_pad.height
        )

    def text_size(
        self,
        text: str,
    ) -> tuple[int, int]:
        text_bbox = self.font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        return (text_width, text_height)

    def table_dimensions(self):
        """
        Returns the dimensions of the table.
        This includes the dimensions of all cells.
        """
        return (self.tab_width, self.tab_height)

    def table_position(self):
        start_xy = (self.margin.left, self.margin.top)
        end_xy = (self.tab_width + self.margin.left, self.tab_height + self.margin.top)
        return (start_xy, end_xy)

    def image_dimensions(self):
        """
        Returns the dimensions of the image.
        """
        return (
            self.tab_width + self.margin.left + self.margin.right,
            self.tab_height + self.margin.top + self.margin.bottom,
        )

    def draw(self) -> Image.Image:
        """
        Draw the table image using Pillow.
        """

        # create image
        image = Image.new(
            "RGBA",
            self.image_dimensions(),
            self.colors.bg,
        )
        draw = ImageDraw.Draw(image)

        ((start_x, start_y), (end_x, end_y)) = self.table_position()

        # add backgrounds (cells and header)
        draw.rectangle(
            [(start_x, start_y), (end_x, end_y)],
            fill=self.colors.cell_bg,
            width=0,
        )

        # add row lines
        y = self.margin.top
        for row_h in self.row_height:
            draw.line(
                [(start_x, y), (end_x, y)],
                fill=self.colors.row_line,
            )
            y += row_h + self.cell_pad.height * 2
        draw.line(
            [(start_x, y), (end_x, y)],
            fill=self.colors.row_line,
        )

        # add column lines
        x = self.margin.left
        for col_w in self.col_width:
            draw.line(
                [(x, start_y), (x, end_y)],
                fill=self.colors.col_line,
            )
            x += col_w + self.cell_pad.width * 2
        draw.line(
            [(x, start_y), (x, end_y)],
            fill=self.colors.col_line,
        )

        (x, y) = (0, self.margin.top + self.cell_pad.height)
        for i, row in enumerate(self.table):
            x = self.margin.left + self.cell_pad.width
            for j, cell in enumerate(row):
                # determine color
                color = self.colors.font
                if self.stock:
                    if cell.startswith("+"):
                        color = self.colors.red
                    elif cell.startswith("-"):
                        color = self.colors.green
                # add text from cell
                draw.text((x, y), cell, font=self.font, fill=color)

                # update position for next cell
                x += self.col_width[j] + self.cell_pad.width * 2
            y += self.row_height[i] + self.cell_pad.height * 2

        return image
