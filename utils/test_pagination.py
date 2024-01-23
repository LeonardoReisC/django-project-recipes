from unittest import TestCase
from parameterized import parameterized
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=1
        )

        self.assertEqual([1, 2, 3, 4], pagination)

    @parameterized.expand([1, 2])
    def test_make_pagination_range_is_static_with_first_pages(self, page):  # noqa: E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=page
        )
        self.assertEqual([1, 2, 3, 4], pagination)
