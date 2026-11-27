const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchProducts(searchTerm = "") {
  const query = searchTerm ? `?search=${encodeURIComponent(searchTerm)}` : "";
  const response = await fetch(`${API_BASE_URL}/api/products${query}`);
  if (!response.ok) {
    throw new Error("Unable to load products");
  }
  return response.json();
}
