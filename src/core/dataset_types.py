import models.datasets


dataset_types = {
    "dendro": {
        "alias": "dendro",
        "name": "Dendrochronology measurement",
        "short": "DENDRO",
        "model": models.datasets.Dendro
    },
    "drms": {
        "alias": "drms",
        "name": "Drilling resistance measurement",
        "short": "DRMS",
        "model": models.datasets.DRMS
    },
    "raman": {
        "alias": "raman",
        "name": "Micro-Raman spectroscopy measurement",
        "short": "MRS",
        "model": models.datasets.Raman
    }
}