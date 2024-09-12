from rasterio.features import shapes
from rio_tiler.io.rasterio import Reader
from rasterio import features
from geopandas import GeoDataFrame
from shapely import geometry
from typing import Any
# Paralelización
from concurrent.futures import ThreadPoolExecutor, as_completed


# TODO: become generic in order to be able to reuse
def crop_raster(raster_path, polygon):
    with Reader(input=raster_path, options={}) as image:
        img = image.feature(polygon)

    return img.render(
        add_mask=True,
        colormap={
            0: (255, 0, 0, 255),
            1: (128, 204, 102, 255),
            2: (232, 214, 107, 255),
        },
    )


# TODO: Test the data resulting from the areas
def get_raster_values(raster_path, polygon, categories) -> dict[str, Any]:
    crs = "EPSG:9377"

    with Reader(input=raster_path, options={}) as cog:


        # Obtener los datos recortados al polígono reproyectado
        data = cog.feature(polygon, dst_crs=crs)
        transform = data.transform
        mask = data.mask != 0

        # Extraer las formas geométricas y valores de los píxeles
        data_shapes = shapes(data.data[0], mask=mask, transform=transform)

        geometries = []
        values = []
        for geom, value in data_shapes:
            geometries.append(geometry.shape(geom))
            values.append(value)

        # Crear un GeoDataFrame para manejar las áreas
        data_frame = GeoDataFrame({"value": values, "geometry": geometries})
        data_frame["area"] = data_frame.geometry.area
        areas = data_frame.groupby("value")["area"].sum() / 10000  # Convertir a hectáreas

        # Filtrar y devolver los datos finales
        output_data = {key: areas[categories[key]] for key in categories if categories[key] in areas}
        return output_data




def parallel_process_rasters(raster_paths, polygon, categories):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_raster_values, path, polygon, categories): path for path in raster_paths}

        for future in as_completed(futures):
            raster_path = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error procesando el archivo raster {raster_path}: {str(e)}")
    return results
