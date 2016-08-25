from django.core.exceptions import ObjectDoesNotExist

from kreddb.models import SiteOptions, Generation, Body, CarImage, IMAGE_SIZES, CarInfo


def _get_car_images(body, generation):
    try:
        original_image = CarImage.objects.get(generation=generation, body=body, main=True).image
    except ObjectDoesNotExist:
        # TODO добавить картинку-заглушку!!!
        return {sz: 'img_stub_' + sz for sz in IMAGE_SIZES}
    return {sz: CarImage.resized_path(original_image.url.rsplit('.', 1), sz) for sz in IMAGE_SIZES}


def _get_price_per_day(body, generation):
    # TODO не нравится мне это место
    price_per_day, created = CarInfo.objects.values_list('price_per_day', flat=True) \
        .get_or_create(generation=generation, body=body)

    if created:
        car_info = price_per_day
        price_per_day = CarInfo.update_price(car_info, generation, body)

    if price_per_day is None:
        price_per_day = CarInfo.find_and_update_price(generation, body)

    return price_per_day


def _create_ui_promo_item(generation: Generation, body: Body):
    return {
        'images': _get_car_images(body, generation),
        'car_make': generation.car_make.name,
        'car_model': generation.car_model.name,
        'url': generation.car_model.filter_url(),
        'price_per_day': _get_price_per_day(body, generation)
    }


def get_promo_items():
    cars = SiteOptions.get_option('promo')

    return [
        _create_ui_promo_item(
            Generation.objects.get(pk=car['gen']),
            Body.objects.get(pk=car['body'])
        )
        for car in cars
        ]


def save_promo_settings(promo_list):
    promo_option = SiteOptions()
    promo_option_value = [
        {
            'gen': promo_item[0],
            'body': promo_item[1]
        } for promo_item in promo_list]
    promo_option.set_option('promo', promo_option_value)
    promo_option.save()
