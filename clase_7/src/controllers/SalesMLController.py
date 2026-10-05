from services.SalesMLPreparationService import SalesMLPreparationService
from dto.SaleMLDTO import SaleMLDTO


class SalesMLController:
    def __init__(self, ml_service: SalesMLPreparationService):
        self.service = ml_service

    def prepare_and_save(self, output_path: str) -> SaleMLDTO:
        return self.service.prepare_and_save(output_path)

    def get_ml_dto(self) -> SaleMLDTO:
        return self.service.transform()