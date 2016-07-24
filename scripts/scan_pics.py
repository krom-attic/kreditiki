import os

top_path = ''
photos = dict()
# scandir не работает с питоном ниже 3.5
for carmake_dir in os.scandir(top_path):
    if not carmake_dir.name.startswith('.') and carmake_dir.is_dir():
        photos[carmake_dir.name] = dict()
        carmake_path = os.path.join(top_path, carmake_dir.name)
        for carmodel_dir in os.scandir(carmake_path):
            carmodel_path = os.path.join(carmake_path, carmodel_dir.name)
            photos[carmake_dir.name][carmodel_dir.name] = carmodel_photos = []
            for dirpath, _, filenames in os.walk(carmodel_path):
                photo_relpath = os.path.relpath(dirpath, carmodel_path)
                for filename in filenames:
                    relpath = os.path.join(photo_relpath, filename)
                    if os.path.splitext(filename)[0] == 'main':
                        carmodel_photos.insert(0, relpath)
                    else:
                        carmodel_photos.append(relpath)
            if os.path.splitext(carmodel_photos[0])[0][-4:] != 'main':
                raise Exception('Не нашли главную фотку!')

