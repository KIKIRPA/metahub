from crud.base import CRUDBase
import models


template = CRUDBase[
    models.Template, 
    models.Template, 
    models.Template]()