from kreddb.bl.image_works import get_car_main_images
from kreddb.models import SiteOptions, CarModel


def _create_ui_promo_item(car_model: CarModel):
    """возвращаем объект для UI"""
    return {
        'images': get_car_main_images(car_model),
        'car_make': car_model.model_family.car_make.name,
        'car_model': car_model.name,
        'url': car_model.get_absolute_url(),
        'price_per_day': car_model.get_price_per_day()
    }


def get_promo_items():
    cars = SiteOptions.get_option('promo')
    promo_items = []
    for car in cars:
        try:
            car_id = int(car['car_model'])
            promo_items.append(_create_ui_promo_item(CarModel.get_by_id(car_id)))
        except ValueError:
            pass
    return promo_items


def save_promo_settings(promo_list):
    promo_option = SiteOptions()
    promo_option_value = [
        {
            'car_model': promo_item,
        } for promo_item in promo_list]
    promo_option.set_option('promo', promo_option_value)
    promo_option.save()
