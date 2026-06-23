import numpy as np
import matplotlib.pyplot as plt

def galaxy_sed(
    wavelengths,
    flux,
    redshift,
    model_params,
    fit_params,
    object_name,
    plot
):
    
    wavelengths = np.asarray(wavelengths)
    flux = np.asarray(flux)

    
    mask = np.isfinite(wavelengths) & np.isfinite(flux)
    wavelengths = wavelengths[mask]
    flux = flux[mask]

    physical_params = {
        "stellar_mass": None,
        "sfr": None,
        "fit_params": None
    }

    
    if plot:
        plt.figure(figsize=(8, 5))
        plt.plot(wavelengths, flux, label="Observed SED")
        plt.plot(wavelengths, flux, label="Fit", linestyle="--")

        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel(" Wavelength")
        plt.ylabel("Flux")
        plt.title(f"SED: {object_name}" if object_name else "Galaxy SED")
        plt.legend()
        plt.show()


    return {
         physical_params
    }