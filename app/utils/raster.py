from rio_tiler.io import Reader


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
