from django.core.paginator import Paginator

import math


def make_pagination_range(page_range, page_qty, current_page):
    total_pages = len(page_range)

    if (page_qty >= total_pages):
        start_range = 0
        stop_range = total_pages
        first_is_out_of_range = False
        last_is_out_of_range = False
    else:
        middle_range = math.ceil(page_qty / 2)
        start_range = current_page - middle_range
        stop_range = current_page + middle_range

        start_range_offset = 0
        if start_range < 0:
            start_range_offset = abs(start_range)
            start_range = 0
            stop_range += start_range_offset

        if stop_range >= total_pages:
            start_range = start_range - abs(total_pages - stop_range)

        first_is_out_of_range = current_page > middle_range
        last_is_out_of_range = stop_range < total_pages

    return {
        'pagination': page_range[start_range:stop_range],
        'page_range': page_range,
        'page_qty': page_qty,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop-range': stop_range,
        'first_page_out_of_range': first_is_out_of_range,
        'last_page_out_of_range': last_is_out_of_range,
    }


def make_pagination(request, queryset, per_page, page_qty=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        page_qty,
        current_page,
    )

    return page_obj, pagination_range
