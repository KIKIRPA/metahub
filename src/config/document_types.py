import models.documents


document_types = {
    "dendro": {
        "alias": "dendro",
        "name": "Dendrochronology measurement",
        "short": "DENDRO",
        "model": models.documents.Dendro
    },
    "drms": {
        "alias": "drms",
        "name": "Drilling resistance measurement",
        "short": "DRMS",
        "model": models.documents.DRMS
    },
    "raman": {
        "alias": "raman",
        "name": "Micro-Raman spectroscopy measurement",
        "short": "MRS",
        "model": models.documents.Raman
    }
}