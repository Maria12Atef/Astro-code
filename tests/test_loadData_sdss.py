import pandas as pd
import pytest

from galaxy_sed.loadData_sdss import load_sdss


def test_load_fits_file(monkeypatch):
    """Test that FITS files are passed to load_sdss_fits."""

    expected = pd.DataFrame({"flux": [1.0]})

    def mock_load_sdss_fits(filepath):
        assert filepath == "galaxy.fits"
        return expected

    monkeypatch.setattr(
        "galaxy_sed.loadData_sdss.load_sdss_fits",
        mock_load_sdss_fits,
    )

    result = load_sdss("galaxy.fits")

    pd.testing.assert_frame_equal(result, expected)


def test_load_dataframe(monkeypatch):
    """Test that DataFrames are passed to convert_sdss_photometry."""

    df = pd.DataFrame({
        "u": [20.1],
        "g": [19.8],
        "r": [19.4],
        "i": [19.2],
        "z": [19.0],
    })

    expected = pd.DataFrame({"flux": [42]})

    def mock_convert_sdss_photometry(data, **kwargs):
        assert data.equals(df)
        return expected

    monkeypatch.setattr(
        "galaxy_sed.loadData_sdss.convert_sdss_photometry",
        mock_convert_sdss_photometry,
    )

    result = load_sdss(df)

    pd.testing.assert_frame_equal(result, expected)


def test_kwargs_are_passed(monkeypatch):
    """Test that keyword arguments are forwarded."""

    df = pd.DataFrame({
        "u": [20],
        "g": [19],
        "r": [18],
        "i": [17],
        "z": [16],
    })

    def mock_convert_sdss_photometry(data, **kwargs):
        assert kwargs["zero_point"] == 3631
        return data

    monkeypatch.setattr(
        "galaxy_sed.loadData_sdss.convert_sdss_photometry",
        mock_convert_sdss_photometry,
    )

    load_sdss(df, zero_point=3631)


def test_invalid_file_extension():
    """Test unsupported file extensions."""

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_sdss("galaxy.csv")


def test_invalid_input_type():
    """Test invalid input types."""

    with pytest.raises(ValueError, match="Input must"):
        load_sdss(12345)