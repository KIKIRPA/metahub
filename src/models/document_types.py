from .documents.dendro import Dendro
from .documents.drms import DRMS
from .documents.raman import Raman


document_types = {
    "dendro": {
        "alias": "dendro",
        "name": "Dendrochronology measurement",
        "short": "DENDRO",
        "model": Dendro
    },
    "drms": {
        "alias": "drms",
        "name": "Drilling resistance measurement",
        "short": "DRMS",
        "model": DRMS
    },
    "raman": {
        "alias": "raman",
        "name": "Micro-Raman spectroscopy measurement",
        "short": "MRS",
        "model": Raman
    }
}