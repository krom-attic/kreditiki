from kreddb.models import CarModel, CarImage


# это для тестовой базы, где есть картинки для моделей, для которых нет модификаций
def create_models():
    for car_image in CarImage.objects.filter(car_model=None):
        car_model, _ = CarModel.objects.get_or_create(
            model_family=car_image.generation.model_family,
            generation=car_image.generation,
            body=car_image.body
        )
        car_image.car_model = car_model
        car_image.save()
