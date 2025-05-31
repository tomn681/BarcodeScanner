#!/bin/bash

# Navega al directorio del script (HouseInventoryV2)
cd "$(dirname "$0")"

# Ejecuta el lector de códigos
python -m barcode_lib.main
