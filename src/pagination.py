import math
from flask import jsonify


class Pagination:
    def __init__(self, rows, per_page, current_page):
        self.total_rows = rows
        self.rows_per_page = per_page
        self.current_page = current_page

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, page):
        if page < 1:
            raise ValueError("Negative values are not allowed in page numbers")
        self._current_page = page

    @property
    def total_pages(self):
        return math.ceil(self.total_rows / self.rows_per_page)

    @property
    def row_offset(self):
        return self.current_page * self.rows_per_page - self.rows_per_page

    @property
    def pages(self):
        return range(1, self.total_pages + 1)

    @property
    def next_page(self):
        return self._get_page_offset(1)

    @property
    def prev_page(self):
        return self._get_page_offset(-1)

    def _get_page_offset(self, offset):
        try:
            offset = self.pages.index(self.current_page + offset)
            return self.pages[offset]
        except ValueError:
            return None

    def get_metadata(self):
        return {"total_pages": self.total_pages, "current_page": self.current_page,
                "prev_page": self.prev_page, "next_page": self.next_page}
