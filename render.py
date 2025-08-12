from PIL import Image, ImageFont, ImageDraw
from collections import namedtuple


def position_tuple(*args):
    Position = namedtuple("Position", ["top", "right", "bottom", "left"])
    if len(args) == 0:
        return Position(0, 0, 0, 0)
    elif len(args) == 1:
        return Position(args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return Position(args[0], args[1], args[0], args[1])
    elif len(args) == 3:
        return Position(args[0], args[1], args[2], args[1])
    else:
        return Position(args[0], args[1], args[2], args[3])


def get_text_size(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont):
    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    return text_width, text_height


def default_colors() -> dict[str, str | None]:
    return {
        "bg": None,
        "cell_bg": "white",
        "header_bg": "gray",
        "font": "black",
        "rowline": "black",
        "colline": "black",
        "red": "red",
        "green": "green",
    }


def draw_table(
    table: list[list[str]],
    header=[],
    font=ImageFont.load_default(),
    cell_pad=(20, 10),
    margin=(10, 10),
    align=None,
    colors=default_colors(),
    stock=False,
):
    """
    Draw a table using Pillow.

    :param table:    A 2D list of strings.
    :param header:   A list of strings.
    :param font:     An ImageFont object.
    :param cell_pad: Padding for cell, (top_bottom, left_right).
    :param margin:   Margin for table, css-like shorthand.
    :param align:    None or list of char, 'l'/'c'/'r' for left/center/right, length must be the max count of columns.
    :param colors:   Dict, as follows.
    :param stock:    Bool, set red/green font color for cells start with +/-.
    """
    _margin = position_tuple(*margin)

    table = table.copy()
    if header:
        table.insert(0, header)
    row_max_hei = [0] * len(table)
    col_max_wid = [0] * len(max(table, key=len))
    for i in range(len(table)):
        for j in range(len(table[i])):
            col_max_wid[j] = max(get_text_size(table[i][j], font)[0], col_max_wid[j])
            row_max_hei[i] = max(get_text_size(table[i][j], font)[1], row_max_hei[i])
    tab_width = sum(col_max_wid) + len(col_max_wid) * 2 * cell_pad[0]
    tab_heigh = sum(row_max_hei) + len(row_max_hei) * 2 * cell_pad[1]

    tab = Image.new(
        "RGBA",
        (
            tab_width + _margin.left + _margin.right,
            tab_heigh + _margin.top + _margin.bottom,
        ),
        colors["bg"],
    )
    draw = ImageDraw.Draw(tab)

    draw.rectangle(
        [
            (_margin.left, _margin.top),
            (_margin.left + tab_width, _margin.top + tab_heigh),
        ],
        fill=colors["cell_bg"],
        width=0,
    )
    if header:
        draw.rectangle(
            [
                (_margin.left, _margin.top),
                (
                    _margin.left + tab_width,
                    _margin.top + row_max_hei[0] + cell_pad[1] * 2,
                ),
            ],
            fill=colors["header_bg"],
            width=0,
        )

    top = _margin.top
    for row_h in row_max_hei:
        draw.line(
            [(_margin.left, top), (tab_width + _margin.left, top)],
            fill=colors["rowline"],
        )
        top += row_h + cell_pad[1] * 2
    draw.line(
        [(_margin.left, top), (tab_width + _margin.left, top)], fill=colors["rowline"]
    )

    left = _margin.left
    for col_w in col_max_wid:
        draw.line(
            [(left, _margin.top), (left, tab_heigh + _margin.top)],
            fill=colors["colline"],
        )
        left += col_w + cell_pad[0] * 2
    draw.line(
        [(left, _margin.top), (left, tab_heigh + _margin.top)], fill=colors["colline"]
    )

    top, left = _margin.top + cell_pad[1], 0
    for i in range(len(table)):
        left = _margin.left + cell_pad[0]
        for j in range(len(table[i])):
            color = colors["font"]
            if stock:
                if table[i][j].startswith("+"):
                    color = colors["red"]
                elif table[i][j].startswith("-"):
                    color = colors["green"]
            _left = left
            if (align and align[j] == "c") or (header and i == 0):
                _left += (col_max_wid[j] - get_text_size(table[i][j], font)[0]) // 2
            elif align and align[j] == "r":
                _left += col_max_wid[j] - get_text_size(table[i][j], font)[0]
            draw.text((_left, top), table[i][j], font=font, fill=color)
            left += col_max_wid[j] + cell_pad[0] * 2
        top += row_max_hei[i] + cell_pad[1] * 2

    return tab
