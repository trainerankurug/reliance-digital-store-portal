import argparse
from collections.abc import Iterable
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from app.models import Product
from app.services.product_service import list_products


class InventoryItem(BaseModel):
    id: int
    name: str
    stock_quantity: int


class ManagerRecommendation(InventoryItem):
    priority: Literal["high", "medium"]
    recommendation: str


class InventoryMonitoringReport(BaseModel):
    total_product_count: int
    out_of_stock_count: int
    low_stock_count: int
    normal_stock_count: int
    out_of_stock_products: list[InventoryItem]
    low_stock_products: list[InventoryItem]
    normal_stock_products: list[InventoryItem]
    manager_attention: list[ManagerRecommendation]


def generate_inventory_report(products: Iterable[Product]) -> InventoryMonitoringReport:
    out_of_stock: list[InventoryItem] = []
    low_stock: list[InventoryItem] = []
    normal_stock: list[InventoryItem] = []

    for product in products:
        if not product.active:
            continue

        item = InventoryItem(
            id=product.id,
            name=product.name,
            stock_quantity=product.stock_quantity,
        )
        if product.stock_quantity == 0:
            out_of_stock.append(item)
        elif product.stock_quantity < 5:
            low_stock.append(item)
        else:
            normal_stock.append(item)

    manager_attention = [
        ManagerRecommendation(
            **item.model_dump(),
            priority="high",
            recommendation="Review this out-of-stock item and assess the appropriate next step.",
        )
        for item in out_of_stock
    ]
    manager_attention.extend(
        ManagerRecommendation(
            **item.model_dump(),
            priority="medium",
            recommendation="Review this low-stock item and determine whether follow-up is needed.",
        )
        for item in low_stock
    )

    return InventoryMonitoringReport(
        total_product_count=len(out_of_stock) + len(low_stock) + len(normal_stock),
        out_of_stock_count=len(out_of_stock),
        low_stock_count=len(low_stock),
        normal_stock_count=len(normal_stock),
        out_of_stock_products=out_of_stock,
        low_stock_products=low_stock,
        normal_stock_products=normal_stock,
        manager_attention=manager_attention,
    )


def run_inventory_monitoring() -> InventoryMonitoringReport:
    return generate_inventory_report(list_products())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a local inventory report.")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path for the local JSON report file; the file must not already exist.",
    )
    args = parser.parse_args()

    report = run_inventory_monitoring()
    with args.output.open("x", encoding="utf-8") as report_file:
        json.dump(report.model_dump(mode="json"), report_file, indent=2)
        report_file.write("\n")

    print(
        json.dumps(
            {
                "report_file": args.output.name,
                "total_product_count": report.total_product_count,
                "out_of_stock_count": report.out_of_stock_count,
                "low_stock_count": report.low_stock_count,
                "normal_stock_count": report.normal_stock_count,
                "manager_attention_count": len(report.manager_attention),
            }
        )
    )


if __name__ == "__main__":
    main()
