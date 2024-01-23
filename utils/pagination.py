import math


def make_pagination_range(page_range, page_qty, current_page):
    middle_range = math.ceil(page_qty / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = 0
    if start_range < 0:
        start_range_offset = abs(start_range)
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    return {
        'pagination': page_range[start_range:stop_range],
        'page_range': page_range,
        'page_qty': page_qty,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop-range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
