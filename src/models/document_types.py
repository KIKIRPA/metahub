from .dendro import Dendro
from .drms import DRMS
from .raman import Raman


document_types = {
    "dendro": {
        "name": "Dendrochronology measurement",
        "short": "DENDRO",
        "model": Dendro
    },
    "drms": {
        "name": "Drilling resistance measurement",
        "short": "DRMS",
        "model": DRMS
    },
    "raman": {
        "name": "Micro-Raman spectroscopy measurement",
        "short": "MRS",
        "model": Raman
    }
}

test_document_templates = {
    "invia_785": {
        "_id": "1",
        "alias": "invia_785",
        "title": "Renishaw inVia, microscope, 785nm",
        "for": "raman",
        "template": {
            "definitions": {
                "MeasurementId": {
                    "properties": {
                        "measurement_technique": {
                            "default": "MRS"
                        }
                    }
                },
                "LaserPower": {
                    "properties": {
                        "neutral_density_filtering": {
                            "default": 0.1,
                            "enum": [100, 50, 10, 5, 1, 0.5, 0.1, 0.05, 0.01]
                        }
                    }
                }
            }
        }
    }
}