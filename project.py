import numpy as np

def clean_photometry(photometry, photometry_errors):
    
    common_filters = set(photometry.keys()) & set(photometry_errors.keys())
    cleaned_flux = {}
    cleaned_errors = {}
    
    for band in common_filters:
        flux = photometry[band]
        error = photometry_errors[band]
        if not (np.isfinite(flux) and np.isfinite(error)):
            continue
        if flux <= 0 or error <= 0:
            continue
        cleaned_flux[band] = flux
        cleaned_errors[band] = error
    
    if not cleaned_flux:
        raise ValueError("No valid photometry data remaining after cleaning.")
    
    return cleaned_flux, cleaned_errors


# ============================================================
# PART 2: CENTRAL ORCHESTRATOR
# ============================================================
def analyse_sed(
    wavelengths,          # Array: effective wavelengths of each flux point (e.g., Angstroms)
    flux,                 # Array: flux densities (e.g., mJy or erg/s/cm2/Hz)
    flux_errors,          # Array: 1-sigma uncertainties for each flux
    redshift,             # Float: galaxy redshift (required to shift models)
    model_params=None,    # Dict: controls the physical model (IMF, dust law, SFH)
    fit_params=None,      # Dict: controls the fitting method (MCMC, grid, steps)
    object_name=None      # String: optional metadata for bookkeeping
):
    """
    Fit galaxy SED from photometric or spectroscopic data.

    Inputs:
        wavelengths  : List/array of effective wavelengths (e.g., [3540, 4770, 6230] Angstroms)
        flux         : List/array of observed fluxes
        flux_errors  : List/array of flux uncertainties
        redshift     : Redshift of the galaxy (float)
        model_params : Dict with keys like 'imf', 'dust_law', 'sfh', 'metallicity'
                       Defaults to {'imf': 'chabrier', 'dust_law': 'calzetti', 'sfh': 'delayed'}
        fit_params   : Dict with keys like 'method', 'n_steps', 'n_walkers'
                       Defaults to {'method': 'chi2', 'n_steps': 1000}
        object_name  : Name or ID of the galaxy (for logging)

    Returns:
        Dictionary with derived physical parameters:
            'stellar_mass'   : in solar masses
            'sfr'            : star formation rate in Msun/yr
            'dust_ebv'       : E(B-V) color excess
            'metallicity'    : Z/Z_solar
            'model_params'   : best-fit model parameters
            'object_name'    : passed through for reference
            'n_bands_used'   : number of valid data points used
    """
    # ------------------------------------------------------------
    # STEP 1: Set default configurations if user didn't provide them
    # ------------------------------------------------------------
    if model_params is None:
        model_params = {
            'imf': 'chabrier',
            'dust_law': 'calzetti',
            'sfh': 'delayed',
            'metallicity': 0.02
        }
    
    if fit_params is None:
        fit_params = {
            'method': 'chi2',    # or 'mcmc'
            'n_steps': 1000,
            'n_walkers': 32
        }

    # ------------------------------------------------------------
    # STEP 2: Validate inputs (basic checks)
    # ------------------------------------------------------------
    # Convert to numpy arrays for safe math
    wavelengths = np.asarray(wavelengths)
    flux = np.asarray(flux)
    flux_errors = np.asarray(flux_errors)
    
    # Check arrays have matching lengths
    if not (len(wavelengths) == len(flux) == len(flux_errors)):
        raise ValueError("wavelengths, flux, and flux_errors must have the same length.")
    
    # Check for NaN / negative values (basic cleaning)
    mask = (np.isfinite(wavelengths) & np.isfinite(flux) & np.isfinite(flux_errors))
    wavelengths = wavelengths[mask]
    flux = flux[mask]
    flux_errors = flux_errors[mask]
    
    if len(wavelengths) == 0:
        raise ValueError("No valid data points after cleaning.")
    
    # Check redshift is valid
    if redshift <= 0:
        raise ValueError("Redshift must be a positive number.")

    # ------------------------------------------------------------
    # STEP 3: (PLACEHOLDER) Generate or load the model SED grid
    # ------------------------------------------------------------
    # Future: model_grid = generate_model_grid(model_params, redshift)
    # This would create model SEDs across a grid of masses, ages, dust values.

    # ------------------------------------------------------------
    # STEP 4: (PLACEHOLDER) Fit the model to the observed data
    # ------------------------------------------------------------
    # Future: best_fit = run_fit(flux, flux_errors, wavelengths, model_grid, fit_params)
    # This would use chi2 or MCMC to find the best parameters.

    # ------------------------------------------------------------
    # STEP 5: (PLACEHOLDER) Derive physical parameters
    # ------------------------------------------------------------
    # Future: result = derive_properties(best_fit, model_params, redshift)
    
    # ------------------------------------------------------------
    # STEP 6: Return a placeholder result
    # ------------------------------------------------------------
    # The return is a dictionary so it's easy to add more keys later.
    return {
        'stellar_mass': 0.0,
        'sfr': 0.0,
        'dust_ebv': 0.0,
        'metallicity': model_params.get('metallicity', 0.0),
        'model_params_used': model_params,
        'fit_params_used': fit_params,
        'object_name': object_name,
        'n_bands_used': len(wavelengths)
    }