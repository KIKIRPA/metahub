from crud.base import CRUDBase
from models.activities.activity import Activity

ActivityUpdate = Activity
ActivityCreate = Activity

activity = CRUDBase[Activity, ActivityCreate, ActivityUpdate]()