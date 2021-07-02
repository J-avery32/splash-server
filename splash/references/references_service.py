from . import NewReference, Reference
from ..service.base import MongoService
from ..users import User
import re


class ReferencesService(MongoService):
    def __init__(self, db, collection_name, create_indexes):
        super().__init__(db, collection_name, create_indexes)

    def create(self, current_user: User, reference: NewReference):
        
        return super().create(current_user=current_user, data=reference)

    def retrieve_one(
        self, current_user: User, uid: str = None, doi: str = None
    ) -> Reference:
        if uid is None and doi is None:
            raise TypeError("either param uid or doi must be a string.")
        if uid is not None and doi is not None:
            raise TypeError("either param uid or doi must be None")
        if uid:
            reference_dict = super().retrieve_one(current_user, uid)
            if reference_dict is None:
                return None
            return Reference(**reference_dict)
        if doi:
            reference_dict = self._collection.find_one({"DOI": doi}, {"_id": False})
            if reference_dict is None:
                return None
            return Reference(**reference_dict)

    def retrieve_multiple(
        self, current_user: User, page: int = 1, query=None, page_size=10, 
    ):
        cursor = super().retrieve_multiple(current_user, page, query, page_size)
        for reference_dict in cursor:
            yield Reference(**reference_dict)

    def search(self, current_user: User, search, page: int = 1, page_size=10):
        query = {
            "$text":{'$search': search}
        }
        return self.retrieve_multiple(
            current_user, page=page, page_size=page_size, query=query
        )

    def update(
        self, current_user: User, data: NewReference, uid: str = None, doi: str = None, etag: str = None
    ):
        old_data_dict = self.retrieve_one(current_user, uid=uid, doi=doi)
        if old_data_dict is None:
            return None
        old_data_dict = old_data_dict.dict()

        return super().update(current_user, data, old_data_dict["uid"], etag=etag)

    def delete(self, current_user: User, uid):
        raise NotImplementedError
