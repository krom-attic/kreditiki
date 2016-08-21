from django.core.exceptions import ObjectDoesNotExist

from kreddb.models import SiteOptions, Generation, Body, CarImage, IMAGE_SIZES


def _get_car_images(body, generation):
    try:
        original_image = CarImage.objects.get(generation=generation, body=body, main=True).image
    except ObjectDoesNotExist:
        # TODO добавить картинку-заглушку!!!
        return {sz: 'img_stub_' + sz for sz in IMAGE_SIZES}
    return {sz: CarImage.resized_path(original_image.url.rsplit('.', 1), sz) for sz in IMAGE_SIZES}


def _create_ui_promo_item(generation: Generation, body: Body):
    return {
        'images': _get_car_images(body, generation),
        'car_make': generation.car_make.name,
        'car_model': generation.car_model.name,
        'url': generation.car_model.filter_url()
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
