import datetime
import os
import random
import string
from decimal import ROUND_HALF_EVEN, Decimal

from django.contrib.auth.models import User
from django.utils.text import slugify


def calculate_nearest_half(decimal_number):   # Swedish rounding
    """
    0.77 -> 0.8   0.74 -> 0.75   0.72 -> 0.7
    """
    return (decimal_number * 2).quantize(Decimal('.1'), ROUND_HALF_EVEN) / Decimal(2)


def get_last_month_data(today):
    """
    Simple method to get the datetime objects for the
    start and end of last month.
    """
    this_month_start = datetime.datetime(today.year, today.month, 1)
    last_month_end = this_month_start - datetime.timedelta(days=1)
    last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
    return last_month_start, last_month_end


def get_month_data_range(months_ago=1, include_this_month=False):
    """
    A method that generates a list of dictionaires
    that describe any given amout of monthly data.
    """
    today = datetime.datetime.now().today()
    dates_ = []
    if include_this_month:
        # get next month's data with:
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        # use next month's data to get this month's data breakdown
        start, end = get_last_month_data(next_month)
        dates_.insert(0, {
            "start": start.timestamp(),
            "end": end.timestamp(),
            "start_json": start.isoformat(),
            "end_json": end.isoformat(),
            "timesince": 0,
            "year": start.year,
            "month": str(start.strftime("%B")),
            })
    for x in range(0, months_ago):
        start, end = get_last_month_data(today)
        today = start
        dates_.insert(0, {
            "start": start.timestamp(),
            "start_json": start.isoformat(),
            "end": end.timestamp(),
            "end_json": end.isoformat(),
            "timesince": int((datetime.datetime.now() - end).total_seconds()),
            "year": start.year,
            "month": str(start.strftime("%B"))
        })
    # dates_.reverse()
    return dates_


def get_filename(path):
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_alphanumeric_string_generator(string_length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(string_length)))


def unique_key_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_vendor_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(10, 20)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(vendor_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_vendor_discount_code_generator(instance):
    """
    This is for a Django project with key field
    """
    key = random_alphanumeric_string_generator(string_length=10).upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(code=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_vendor_guest_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(5, 10)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(guest_vendor_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance, range_from=100000000000, range_until=1000000000000):
    """
    This is for a Django project with order_id field
    """

    new_order_id = random.randrange(range_from, range_until)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id


def unique_customer_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(10, 15)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(customer_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_customer_discount_code_generator(instance):
    """
    This is for a Django project with key field
    """
    key = random_alphanumeric_string_generator(string_length=10).upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(code=key).exists()
    if qs_exists:
        return unique_customer_discount_code_generator(instance)
    return key


def unique_product_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(5, 15)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(product_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_cart_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(10, 20)
    key = random_string_generator(size=size).upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(cart_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance).upper()
    return key


def unique_cart_item_id_generator(instance):
    """
    This is for a Django project with key field
    """
    size = random.randint(10, 30)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(item_id=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_vendor_customer_username_generator():
    prefix = 'vendorcustomer'
    random_number = random.randrange(100000, 1000000)
    username = prefix + str(random_number)
    qs_exists = User.objects.filter(username=username).exists()
    if qs_exists:
        return unique_vendor_customer_username_generator()
    return username


def unique_guest_vendor_username_generator():
    prefix = 'guestvendor'
    random_number = random.randrange(100000, 1000000)
    username = prefix + str(random_number)
    qs_exists = User.objects.filter(username=username).exists()
    if qs_exists:
        return unique_vendor_customer_username_generator()
    return username
