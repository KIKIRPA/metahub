from crud.base import CRUDBase
import models.activities


activity = CRUDBase[
    models.activities.Activity, 
    models.activities.Activity, 
    models.activities.Activity]()

intervention_file = CRUDBase[
    models.activities.InterventionFile, 
    models.activities.InterventionFile, 
    models.activities.InterventionFile]()

project = CRUDBase[
    models.activities.Project, 
    models.activities.Project, 
    models.activities.Project]()