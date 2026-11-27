import json
import subprocess
import sys

from fastapi.testclient import TestClient

from app.agents.inventory_monitoring_agent import generate_inventory_report
from app.main import app
from app.models import Product

client = TestClient(app)


def make_product(
    product_id: int,
    name: str,
    stock_quantity: int,
    *,
    active: bool = True,
) -> Product:
    return Product(
        id=product_id,
        name=name,
        category="Synthetic",
        price=999.0,
        stock_quantity=stock_quantity,
        active=active,
    )


def test_report_classifies_stock_boundaries_and_excludes_inactive_products():
    report = generate_inventory_report(
        [
            make_product(201, "Sample Out", 0),
            make_product(202, "Sample Low", 1),
            make_product(203, "Sample Low Boundary", 4),
            make_product(204, "Sample Normal Boundary", 5),
            make_product(205, "Sample Normal", 20),
            make_product(206, "Inactive Sample", 0, active=False),
        ]
    )

    assert report.total_product_count == 5
    assert report.out_of_stock_count == 1
    assert report.low_stock_count == 2
    assert report.normal_stock_count == 2
    assert [item.id for item in report.out_of_stock_products] == [201]
    assert [item.id for item in report.low_stock_products] == [202, 203]
    assert [item.id for item in report.normal_stock_products] == [204, 205]
    assert [item.id for item in report.manager_attention] == [201, 202, 203]
    assert [item.priority for item in report.manager_attention] == [
        "high",
        "medium",
        "medium",
    ]


def test_inventory_monitoring_endpoint_uses_active_catalog_and_omits_prices():
    response = client.get("/api/agents/inventory-monitoring")

    assert response.status_code == 200
    report = response.json()
    assert report["total_product_count"] == 4
    assert report["out_of_stock_count"] == 1
    assert report["low_stock_count"] == 1
    assert report["normal_stock_count"] == 2
    product_groups = (
        "out_of_stock_products",
        "low_stock_products",
        "normal_stock_products",
    )
    assert all(
        set(item) == {"id", "name", "stock_quantity"}
        for group in product_groups
        for item in report[group]
    )
    assert all(
        set(item)
        == {
            "id",
            "name",
            "stock_quantity",
            "priority",
            "recommendation",
        }
        for item in report["manager_attention"]
    )
    assert all(
        "price" not in item
        for group in (*product_groups, "manager_attention")
        for item in report[group]
    )


def test_local_report_cli_keeps_product_details_out_of_console_output(tmp_path):
    report_path = tmp_path / "inventory-report.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app.agents.inventory_monitoring_agent",
            "--output",
            str(report_path),
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary == {
        "report_file": report_path.name,
        "total_product_count": 4,
        "out_of_stock_count": 1,
        "low_stock_count": 1,
        "normal_stock_count": 2,
        "manager_attention_count": 2,
    }
    assert "Wireless Headphones" not in result.stdout
    assert "2499" not in result.stdout

    local_report = json.loads(report_path.read_text(encoding="utf-8"))
    assert local_report["low_stock_products"][0]["name"] == "Wireless Headphones"
    assert "price" not in local_report["low_stock_products"][0]
