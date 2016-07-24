from io import BytesIO
from zipfile import ZipFile

from django.core.files.images import ImageFile

from kreddb.models import GenerationImage, Generation, CarMake, CarModel


def is_directory(fileinfo):
    return fileinfo.orig_filename.endswith('/')


def fix_zip_string(string):
    return string.encode('437').decode('866')


def fake_import_images(file, car_make_name=None, car_model_name=None, gen_years=None):
    max_depth = 3
    offset = 0

    params = []

    if car_make_name is not None:
        params.append(CarMake.get_by_name(car_make_name))
        offset = 1
        if car_model_name is not None:
            params.append(CarModel.get_by_name(car_model_name, params[0]))
            offset = 2
            if gen_years is not None:
                params.append(Generation.get_by_year(params[1], gen_years[0], gen_years[1]))
                offset = 3

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
                gen_parts = path_parts.pop().split(' ', 1)
                gen_years = gen_parts[0].split('-', 1)
                if len(gen_parts) > 1:
                    gen_years.append(fix_zip_string(gen_parts[1]))
                else:
                    gen_years.append('')
                params.append(Generation.get_by_year(params[1], gen_years[0], gen_years[1]))
        else:
            with zf.open(fileinfo) as image_file:
                generation_image = GenerationImage(generation=params[-1])
                # Заодно сохранет и сам объект, поскольку save=True
                generation_image.image.save(
                    fix_zip_string('_'.join(path_parts[max_depth - offset:])),
                    ImageFile(BytesIO(image_file.read()))
                )
