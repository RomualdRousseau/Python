from io import StringIO


class Code:
    def __init__(self):
        self.src_lines = None

    def load_from_file(self, path):
        with open(path, "r") as f:
            self.src_lines = f.readlines()

    def get_str_at(self, point):
        row, column = point
        if row >= len(self.src_lines) or column >= len(self.src_lines[row]):
            return None
        return self.src_lines[row][column:]

    def get_bytes_at(self, point):
        c = self.get_str_at(point)
        return c.encode("utf8") if c != None else None

    def get_block_between(self, start_point, end_point, show_line_numbers=True):
        start_y, _ = start_point
        end_y, _ = end_point
        with StringIO() as buffer:
            for y in range(start_y, end_y + 1):
                if show_line_numbers:
                    buffer.write(str(y).rjust(3, "0"))
                    buffer.write(" ")
                buffer.write(self.get_str_at((y, 0)))
            return buffer.getvalue()
