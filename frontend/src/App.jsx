import { useEffect, useState } from "react";
import { fetchProducts } from "./api.js";

export default function App() {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function loadProducts() {
      try {
        setIsLoading(true);
        const result = await fetchProducts(searchTerm);
        if (isMounted) {
          setProducts(result);
          setErrorMessage("");
        }
      } catch (error) {
        if (isMounted) {
          setErrorMessage(error.message);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadProducts();
    return () => {
      isMounted = false;
    };
  }, [searchTerm]);

  return (
    <main style={{ fontFamily: "Arial, sans-serif", margin: "2rem auto", maxWidth: 900, padding: "0 1rem" }}>
      <h1>Reliance Digital – Store Operations</h1>
      <p>Product catalogue and inventory overview</p>

      <label htmlFor="product-search">Search products</label>
      <input
        id="product-search"
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
        placeholder="Search by product name"
        style={{ display: "block", margin: "0.5rem 0 1.5rem", padding: "0.6rem", width: "min(100%, 360px)" }}
      />

      {isLoading && <p>Loading products...</p>}
      {errorMessage && <p role="alert">{errorMessage}</p>}

      {!isLoading && !errorMessage && (
        <table cellPadding="10" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th align="left">Product</th>
              <th align="left">Category</th>
              <th align="right">Price (INR)</th>
              <th align="right">Available stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id} style={{ borderTop: "1px solid #ddd" }}>
                <td>{product.name}</td>
                <td>{product.category}</td>
                <td align="right">{product.price.toLocaleString("en-IN")}</td>
                <td align="right">{product.stock_quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!isLoading && !errorMessage && products.length === 0 && <p>No products found.</p>}
    </main>
  );
}
