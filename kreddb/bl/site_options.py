from django.core.exceptions import ObjectDoesNotExist

from kreddb.models import SiteOptions, CarImage, IMAGE_SIZES, CarModel


def _get_car_images(car_model: CarModel):
    try:
        original_image = CarImage.objects.get(car_model=car_model, main=True).image
    except ObjectDoesNotExist:
        # TODO добавить картинку-заглушку!!!
        return {sz: 'img_stub_' + sz for sz in IMAGE_SIZES}
    return {sz: CarImage.resized_path(original_image.url.rsplit('.', 1), sz) for sz in IMAGE_SIZES}


def get_price_per_day(car_model: CarModel):
    if car_model.price_per_day is None:
        return car_model.update_price()
    else:
        return car_model.price_per_day


def _create_ui_promo_item(car_model: CarModel):
    # возвращаем объект для UI
    return {
        'images': _get_car_images(car_model),
        'car_make': car_model.model_family.car_make.name,
        'car_model': car_model.name,
        'url': car_model.get_absolute_url(),
        'price_per_day': get_price_per_day(car_model)
    }


def get_promo_items():
    cars = SiteOptions.get_option('promo')

    return [
        _create_ui_promo_item(
            CarModel.objects.get(pk=car['car_model']),
        )
        for car in cars
        ]


def save_promo_settings(promo_list):
    promo_option = SiteOptions()
    promo_option_value = [
        {
            'car_model': promo_item,
        } for promo_item in promo_list]
    promo_option.set_option('promo', promo_option_value)
    promo_option.save()
