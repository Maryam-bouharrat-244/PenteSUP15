import os
import rasterio
import numpy as np

# Chemins
mnt_dir = r"C:\Users\marya\OneDrive - FF NEW ENERGY VENTURE S.A\FFNEV France - 01_General\06_SIG\01_data_generales\national\MNT_Pentes\MNT"
output_dir = r"C:\Users\marya\OneDrive - FF NEW ENERGY VENTURE S.A\FFNEV France - 01_General\06_SIG\01_data_generales\national\MNT_Pentes\PENTE_SUP15"
os.makedirs(output_dir, exist_ok=True)

# Parcourir tous les fichiers MNT du dossier
for filename in os.listdir(mnt_dir):
    if filename.lower().endswith(('.tif', '.tiff')) and filename.startswith('MNT_D'):
        mnt_path = os.path.join(mnt_dir, filename)
        with rasterio.open(mnt_path) as src:
            arr = src.read(1).astype(float)
            # Calcul de la pente (en %)
            x, y = np.gradient(arr, src.res[0], src.res[1])
            slope = np.sqrt(x**2 + y**2) * 100
            # Masquer les valeurs nodata
            if src.nodata is not None:
                slope[arr == src.nodata] = np.nan
            # Extraire zones > 15%
            pente_sup15 = (slope > 15).astype(np.uint8)
            # Mettre 255 là où c'est nodata
            pente_sup15[np.isnan(slope)] = 255
            # Préparer les métadonnées de sortie
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "dtype": 'uint8',
                "count": 1,
                "nodata": 255
            })
            # Sauvegarder
            out_file = os.path.join(output_dir, filename.replace('MNT_', 'PENTE_SUP15_'))
            with rasterio.open(out_file, "w", **out_meta) as dest:
                dest.write(pente_sup15, 1)
        print(f"Fichier traité : {filename}")
print("Traitement terminé. Les rasters sont dans :", output_dir)
