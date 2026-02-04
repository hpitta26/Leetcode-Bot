import { Link, useNavigate, useLocation } from 'react-router-dom'

function Navbar({ activeTab, setActiveTab }) {
  const navigate = useNavigate()
  const location = useLocation()
  const isProfilePage = location.pathname.startsWith('/profile/')

  const handleTabClick = (tab) => {
    setActiveTab(tab)
    if (isProfilePage) {
      navigate('/')
    }
  }

  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto">
        <div className="relative flex items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              Reach TIP Leaderboard
            </Link>
          </div>
          
          {/* Tabs - Centered */}
          <div className="absolute left-1/2 transform -translate-x-1/2 flex space-x-8">
            <button
              onClick={() => handleTabClick('weekly')}
              className={`px-4 py-2 font-medium transition-all relative ${
                activeTab === 'weekly'
                  ? 'text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              Weekly
              {activeTab === 'weekly' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 dark:bg-blue-400"></div>
              )}
            </button>
            <button
              onClick={() => handleTabClick('all_time')}
              className={`px-4 py-2 font-medium transition-all relative ${
                activeTab === 'all_time'
                  ? 'text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              All Time
              {activeTab === 'all_time' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 dark:bg-blue-400"></div>
              )}
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

