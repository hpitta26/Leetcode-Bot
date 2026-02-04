import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'

function Profile() {
  const { username } = useParams()
  const [userData, setUserData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data - in production, fetch from API
    // Simulating data fetch
    const mockData = {
      'BanditPanda6': {
        username: 'BanditPanda6',
        rank: 229,
        score: 2437.4,
        country: 'United States',
        state: 'Florida',
        university: 'Florida International University',
        weekly: {
          rank: 1,
          totalScore: 1,
          solutions: { A: true, B: false, C: false }
        },
        allTime: {
          rank: 1,
          totalScore: 245,
          easySolved: 120,
          mediumSolved: 85,
          hardSolved: 40
        }
      },
      'gpena1': {
        username: 'gpena1',
        rank: 347,
        score: 1856.2,
        country: 'United States',
        state: 'Florida',
        university: 'Florida International University',
        weekly: {
          rank: 2,
          totalScore: 0,
          solutions: { A: false, B: false, C: false }
        },
        allTime: {
          rank: 2,
          totalScore: 189,
          easySolved: 95,
          mediumSolved: 68,
          hardSolved: 26
        }
      }
    }

    setTimeout(() => {
      setUserData(mockData[username])
      setLoading(false)
    }, 300)
  }, [username])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading profile...</p>
        </div>
      </div>
    )
  }

  if (!userData) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400 text-xl">User not found</p>
        </div>
      </div>
    )
  }

  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 
           name.slice(0, 2).toUpperCase()
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden mb-8">
          {/* Profile Header */}
          <div className="p-6">
            <div className="flex items-center justify-between">
              {/* Left side: Avatar and Name */}
              <div className="flex items-center gap-4">
                {/* Avatar */}
                <div className="w-16 h-16 bg-gray-100 dark:bg-gray-900 rounded-full flex items-center justify-center border-2 border-gray-200 dark:border-gray-700">
                  <span className="text-xl font-bold text-gray-900 dark:text-white">
                    {getInitials(userData.username)}
                  </span>
                </div>
                {/* Name */}
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {userData.username}
                  </h1>
                </div>
              </div>

              {/* Right side: Stats */}
              <div className="flex items-center gap-6">
                <div className="text-right">
                  <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Rank</div>
                  <div className="text-xl font-bold text-gray-900 dark:text-white">{userData.rank}</div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">Score</div>
                  <div className="text-xl font-bold text-gray-900 dark:text-white">{userData.score}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
  )
}

export default Profile

