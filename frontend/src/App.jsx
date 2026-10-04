import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Navbar from './components/Navbar'

import Home from './pages/Home'
import CropRecommendation from './pages/CropRecommendation'
import SoilHealth from './pages/SoilHealth'
import Fertilizer from './pages/Fertilizer'
import Reports from './pages/Reports'
import ReportDetail from './pages/ReportDetail'

import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/crop-recommendation"
          element={<CropRecommendation />}
        />

        <Route
          path="/soil-health"
          element={<SoilHealth />}
        />

        <Route
          path="/fertilizer"
          element={<Fertilizer />}
        />

        <Route
          path="/reports"
          element={<Reports />}
        />

        <Route
          path="/reports/:id"
          element={<ReportDetail />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App