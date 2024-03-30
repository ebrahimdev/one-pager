import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const base_url = 'http://localhost:5000'
  const [product, setProduct] = useState({});

  useEffect(() => {
    fetch(`${base_url}/product`)
      .then(response => response.json())
      .then(data => setProduct(data))
      .catch(error => console.error("There was an error!", error));
  }, []);


  return (
    <div className="App">
      {product.imageResourceUrl && (<>
        <div className="header">
          <h1>{product.storeName}</h1>
        </div>
        <div className="container">
          <div className="product-card">
            <img src={`${base_url}/product/image?resource_url=${encodeURIComponent(product.imageResourceUrl)}`} alt="Product" alt={product.name} className="product-image" />
            <div className="product-info">
              <h2>{product.name}</h2>
              <p>{product.description}</p>
              <p className="price">{product.price}</p>
              <a href="#" className="buy-now">Buy Now</a>
            </div>
          </div>
        </div>
      </>
      )}

    </div>
  );
}

export default App;
