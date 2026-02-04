import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react'
import Home from './pages/Home'
import Profile from './pages/Profile'
import Navbar from './components/Navbar'
import Banner from './components/Banner'

function Layout() {
  const [activeTab, setActiveTab] = useState('weekly')
  
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      <Banner />
      
      <Routes>
        <Route path="/" element={<Home activeTab={activeTab} />} />
        <Route path="/profile/:username" element={<Profile />} />
      </Routes>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  )
}

export default App
