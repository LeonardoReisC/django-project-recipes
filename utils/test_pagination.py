from unittest import TestCase
from parameterized import parameterized
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=1
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    @parameterized.expand([1, 2])
    def test_make_pagination_range_is_static_with_first_pages(self, page):  # noqa: E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=page
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    @parameterized.expand([4, 10, 18])
    def test_make_pagination_range_changes_with_middle_pages(self, page):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=page
        )['pagination']
        page_list = list(range(page-1, page+3))

        self.assertEqual(page_list, pagination)

    @parameterized.expand([19, 20, 21])
    def test_make_pagination_range_is_static_with_last_pages(self, page):  # noqa: E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=page
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
