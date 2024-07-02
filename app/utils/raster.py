from rio_tiler.io import Reader
import numpy


# TODO: become generic in order to be able to reuse
def crop_raster(raster_path, polygon):
    with Reader(raster_path) as image:
        img = image.feature(polygon)

    return img.render(
        add_mask=True,
        colormap={
            0: (255, 0, 0, 255),
            1: (128, 204, 102, 255),
            2: (232, 214, 107, 255),
        },
    )


def get_raster_values(raster_path, polygon):
    categories = {"Perdida": 0, "Persistencia": 1, "No bosque": 2}

    with Reader(raster_path) as cog:
        data, mask = cog.feature(polygon)
        masked_data = numpy.ma.masked_array(data, mask=~mask).astype(
            numpy.int32
        )
        unique_values, counts = numpy.unique(
            masked_data.compressed(), return_counts=True
        )
        values = dict(zip(unique_values, counts))
        lista_combinada = [
            {"key": key, "value": int(values[categories[key]])}
            for key in categories
        ]
        return lista_combinada
