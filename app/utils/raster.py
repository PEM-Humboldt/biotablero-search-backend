import io

import rasterio
from rasterio.mask import mask
from matplotlib import pyplot as plt, colors


# TODO: become generic in order to be able to reuse
def crop_raster(raster_path, polygon):
    with rasterio.open(raster_path) as src:
        out_image, out_transform = mask(src, [polygon], crop=True, nodata=3)
        out_meta = src.meta.copy()
    out_meta.update(
        {
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": 3,
        }
    )
    return out_image, out_meta


# TODO: become generic in order to be able to reuse
def get_binaries_png(raster_data, raster_metadata):
    cmap_colors = [
        (1.0, 0.0, 0.0),
        (0.5, 0.8, 0.4),
        (0.91, 0.84, 0.42),
        (1, 1, 1),
    ]
    cmap = colors.ListedColormap(cmap_colors)

    cmap.set_bad(alpha=0.0)
    fig, ax = plt.subplots(
        figsize=(
            raster_metadata["width"] / 100,
            raster_metadata["height"] / 100,
        )
    )
    ax.axis("off")
    ax.imshow(
        raster_data[0],
        cmap=cmap,
        extent=[
            raster_metadata["transform"][2],
            raster_metadata["transform"][2]
            + raster_metadata["width"] * raster_metadata["transform"][0],
            raster_metadata["transform"][5]
            + raster_metadata["height"] * raster_metadata["transform"][4],
            raster_metadata["transform"][5],
        ],
        interpolation="nearest",
    )

    buf = io.BytesIO()
    plt.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
        transparent=True,
    )
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()
