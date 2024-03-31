import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProductPage from './components/product-page/product-page';

function App() {
  return (
    <Routes>
      <Route path="/:productId" element={<ProductPage />} />
    </Routes>
  );
}

export default App;
