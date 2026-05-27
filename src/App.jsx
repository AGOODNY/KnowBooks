import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Landing from './pages/Landing'
import Home from './pages/Home'
import Search from './pages/Search'
import BookDetail from './pages/BookDetail'
import Upload from './pages/Upload'
import Profile from './pages/Profile'
import Admin from './pages/Admin'
import Recommend from './pages/Recommend'

function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/home" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/book/:id" element={<BookDetail />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/recommend" element={<Recommend />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
