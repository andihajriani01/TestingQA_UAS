import json

from .settings import DEFAULT_PRICE

def test_product_detail_api(client):
    id = 3
    response = client.get(f"/api/products/{id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert id == data.get('id')
    assert DEFAULT_PRICE * id == data.get('price')  # Memperbaiki bagian ini


def test_product_api(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Memastikan bahwa data yang dikembalikan adalah list


# post new cart
def test_post_cart(client):
    product_id = 1
    quantity = 2
    response = client.post("/api/cart", json={"product_id": product_id, "quantity": quantity})
    assert response.status_code == 201  # Memastikan bahwa cart berhasil dibuat

    # Memeriksa apakah cart memiliki item yang benar
    data = json.loads(response.data)
    assert "cart_id" in data
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == quantity


# additional test for updating cart
def test_update_cart(client):
    product_id = 1
    quantity = 2

    # Post new cart
    response = client.post("/api/cart", json={"product_id": product_id, "quantity": quantity})
    assert response.status_code == 201

    data = json.loads(response.data)
    cart_id = data["cart_id"]

    # Update cart
    new_quantity = 3
    response = client.put(f"/api/cart/{cart_id}", json={"product_id": product_id, "quantity": new_quantity})
    assert response.status_code == 200

    # Check if the cart is updated correctly
    updated_data = json.loads(response.data)
    assert updated_data["cart_id"] == cart_id
    assert len(updated_data["items"]) == 1
    assert updated_data["items"][0]["product_id"] == product_id
    assert updated_data["items"][0]["quantity"] == new_quantity


# additional test for deleting cart
def test_delete_cart(client):
    product_id = 1
    quantity = 2

    # Post new cart
    response = client.post("/api/cart", json={"product_id": product_id, "quantity": quantity})
    assert response.status_code == 201

    data = json.loads(response.data)
    cart_id = data["cart_id"]

    # Delete cart
    response = client.delete(f"/api/cart/{cart_id}")
    assert response.status_code == 204

    # Check if the cart is deleted
    response = client.get(f"/api/cart/{cart_id}")
    assert response.status_code == 404
