from io import BytesIO
from zipfile import ZipFile

from django.core.files.images import ImageFile
from django.db import transaction

from kreddb.models import CarImage, Generation, CarMake, Body, CarModel


def is_directory(fileinfo):
    return fileinfo.orig_filename.endswith('/')


def fix_zip_string(string):
    return string.encode('437').decode('866')


@transaction.atomic
def import_images(file, car_make_name=None, car_model_name=None, gen_start_year=None, car_body=None):
    max_depth = 4
    offset = 0

    params = []

    if car_make_name is not None:
        params.append(CarMake.get_by_name(car_make_name))
        offset = 1
        if car_model_name is not None:
            params.append(car_model_name)
            offset = 2
            if gen_start_year is not None:
                params.append(Generation.get_by_year(params[1], gen_start_year))
                offset = 3
                if car_body is not None:
                    params.append(Body.get_by_name_loose(car_body))

    zf = ZipFile(file)

    for fileinfo in sorted(zf.infolist(), key=lambda e: e.orig_filename):
        path_parts = fileinfo.orig_filename.strip('/').split('/')
        if is_directory(fileinfo):
            if len(path_parts) > max_depth - offset:
                continue
            idx = len(path_parts) + offset - 1
            params = params[:idx]
            if idx == 0:
                car_make_name = path_parts.pop()
                params.append(CarMake.get_by_name(fix_zip_string(car_make_name)))
            elif idx == 1:
                car_model_name = path_parts.pop()
                params.append(fix_zip_string(car_model_name))
            elif idx == 2:
                gen_start_year = path_parts.pop()
                # TODO вынести этот код в модель
                first_car_model = CarModel.objects.filter(model_family__car_make=params[0], name=params[1]).first()
                if first_car_model is None:
                    raise CarModel.DoesNotExist
                model_family = first_car_model.model_family
                params.append(Generation.get_by_year(model_family, gen_start_year))
            elif idx == 3:
                car_body = path_parts.pop()
                params.append(Body.get_by_name_loose(fix_zip_string(car_body)))
        else:
            car_model = CarModel.get_by_name(name=params[-3], generation=params[-2], body=params[-1])
            with zf.open(fileinfo) as image_file:
                car_image = CarImage(car_model=car_model)
                # Заодно сохранет и сам объект, поскольку save=True
                image_file = ImageFile(BytesIO(image_file.read()))
                car_image.image.save(
                    fix_zip_string('_'.join(path_parts[max_depth - offset:])),
                    image_file
                )
                image_file.close()
