from kreddb.models import CarImage, CarModel, IMAGE_SIZES


def get_car_main_images(car_model: CarModel):
    try:
        original_image = CarImage.get_main_car_image(car_model)
    except CarImage.DoesNotExist:
        # TODO добавить картинку-заглушку!!!
        return {sz: 'img_stub_' + sz for sz in IMAGE_SIZES}
    return {sz: CarImage.resized_path(original_image.url.rsplit('.', 1), sz) for sz in IMAGE_SIZES}
