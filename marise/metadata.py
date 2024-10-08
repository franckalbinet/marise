"""Parse MARIS NetCDF files metadata, index and query them using Ragatouille."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_metadata.ipynb.

# %% auto 0
__all__ = ['SEPARATOR_LENGTH', 'SEPARATOR', 'read_metadata', 'read_metadata_from_directory', 'dict_to_string']

# %% ../nbs/00_metadata.ipynb 3
import netCDF4 as nc
from pathlib import Path
from fastcore.all import *
from ragatouille import RAGPretrainedModel

# %% ../nbs/00_metadata.ipynb 4
SEPARATOR_LENGTH = 80
SEPARATOR = f"{'-'*SEPARATOR_LENGTH}"

# %% ../nbs/00_metadata.ipynb 5
def read_metadata(fname):
    "Read a netcdf metadata file using netcdf4 package"    
    try:
        with nc.Dataset(fname, 'r') as dataset:
            global_attrs = {attr: dataset.getncattr(attr) for attr in dataset.ncattrs()}
            variables = {}
            for var_name, var in dataset.variables.items():
                variables[var_name] = {
                    'dimensions': var.dimensions,
                    'attributes': {attr: var.getncattr(attr) for attr in var.ncattrs()},
                    'dtype': var.dtype,
                    'shape': var.shape
                }
            metadata = {
                'global_attributes': global_attrs,
                # 'variables': variables
            }
            
        return metadata
    
    except Exception as e:
        print(f"Error reading NetCDF file: {e}")
        return None

# %% ../nbs/00_metadata.ipynb 7
def read_metadata_from_directory(
    src_dir:str, # Directory containing NetCDF files",
    recursive:bool=False # Search recursively in subdirectories
) -> list:
    "Read metadata from all NetCDF files in the given directory."
    src_dir = Path(src_dir)
    pattern = '**/*.nc' if recursive else '*.nc'
    return [{'fname': f.name, 'value': read_metadata(f)}  for f in src_dir.glob(pattern)]

# %% ../nbs/00_metadata.ipynb 10
def dict_to_string(d, indent=0):
    """Convert a dictionary to a formatted string."""
    result = []
    for key, value in d.items():
        result.append(' ' * indent + str(key) + ': ')
        if isinstance(value, dict):
            result.append('\n' + dict_to_string(value, indent + 2))
        else:
            result.append(str(value) + '\n')
    return ''.join(result)
