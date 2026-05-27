import { Link, useNavigate, useLocation } from 'react-router-dom'
import SearchBar from './SearchBar'
import './Navbar.css'

function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()
  const isLanding = location.pathname === '/'

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="navbar-left">
          {!isLanding && (
            <button
              className="nav-back-btn"
              onClick={() => window.history.back()}
              title="Go back"
            >
              ←
            </button>
          )}
          <Link to={isLanding ? '/' : '/home'} className="navbar-brand">
            KnowBooks
          </Link>
        </div>

        {!isLanding && (
          <div className="navbar-center">
            <SearchBar />
          </div>
        )}

        <div className="navbar-right">
          {isLanding ? (
            <>
              <button className="btn-text" onClick={() => navigate('/home')}>Log in</button>
              <button className="btn-primary btn-sm" onClick={() => navigate('/home')}>Sign up</button>
            </>
          ) : (
            <div className="navbar-user">
              <div className="user-avatar">U</div>
              <span className="user-name">User</span>
              <div className="user-dropdown">
                <Link to="/profile">Profile</Link>
                <Link to="/upload">My Uploads</Link>
                <Link to="/admin">Admin</Link>
                <hr />
                <button className="btn-logout">Log out</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
