from io import BytesIO
from zipfile import ZipFile

from django.core.files.images import ImageFile

from kreddb.models import CarImage, Generation, CarMake, CarModel, Body


def is_directory(fileinfo):
    return fileinfo.orig_filename.endswith('/')


def fix_zip_string(string):
    return string.encode('437').decode('866')


def import_images(file, car_make_name=None, car_model_name=None, gen_start_year=None, car_body=None):
    max_depth = 4
    offset = 0

    params = []

    if car_make_name is not None:
        params.append(CarMake.get_by_name(car_make_name))
        offset = 1
        if car_model_name is not None:
            params.append(CarModel.get_by_name(car_model_name, params[0]))
            offset = 2
            if gen_start_year is not None:
                params.append(Generation.get_by_year(params[1], gen_start_year))
                offset = 3
                if car_body is not None:
                    params.append(Body.get_by_name(car_body))

    zf = ZipFile(file)

    for fileinfo in zf.infolist():
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
                params.append(CarModel.get_by_name(fix_zip_string(car_model_name), params[0]))
            elif idx == 2:
                gen_start_year = path_parts.pop()
                params.append(Generation.get_by_year(params[1], gen_start_year))
            elif idx == 3:
                car_body = path_parts.pop()
                params.append(Body.get_by_name(fix_zip_string(car_body)))
        else:
            with zf.open(fileinfo) as image_file:
                car_image = CarImage(generation=params[-2], body=params[-1])
                # Заодно сохранет и сам объект, поскольку save=True
                car_image.image.save(
                    fix_zip_string('_'.join(path_parts[max_depth - offset:])),
                    ImageFile(BytesIO(image_file.read()))
                )
