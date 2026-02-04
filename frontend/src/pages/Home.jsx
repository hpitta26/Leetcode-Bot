import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Home({ activeTab }) {
  const [competition, setCompetition] = useState(null)
  const [problems, setProblems] = useState([])
  const [leaderboard, setLeaderboard] = useState([])
  const [allTimeLeaderboard, setAllTimeLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setCompetition({
      name: 'Week 5',
      startDate: '2026-02-07',
      endDate: '2026-02-14'
    })

    setProblems([
      { letter: 'A', title: 'Two Sum', difficulty: 'Easy' },
      { letter: 'B', title: 'Add Two Numbers', difficulty: 'Medium' },
      { letter: 'C', title: 'Median of Two Sorted Arrays', difficulty: 'Hard' }
    ])

    setLeaderboard([
      { 
        rank: 1, 
        username: 'BanditPanda6', 
        totalScore: 1, 
        problemsSolved: 1,
        solutions: { A: true, B: false, C: false }
      },
      { 
        rank: 2, 
        username: 'gpena1', 
        totalScore: 0, 
        problemsSolved: 0,
        solutions: { A: false, B: false, C: false }
      }
    ])

    setAllTimeLeaderboard([
      {
        rank: 1,
        username: 'BanditPanda6',
        totalScore: 245,
        easySolved: 120,
        mediumSolved: 85,
        hardSolved: 40
      },
      {
        rank: 2,
        username: 'gpena1',
        totalScore: 189,
        easySolved: 95,
        mediumSolved: 68,
        hardSolved: 26
      }
    ])

    setLoading(false)
  }, [])

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-600 dark:text-green-400'
      case 'Medium': return 'text-yellow-600 dark:text-yellow-400'
      case 'Hard': return 'text-red-600 dark:text-red-400'
      default: return 'text-gray-600 dark:text-gray-400'
    }
  }

  if (loading) {
  return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className={`grid grid-cols-1 gap-8 ${activeTab === 'weekly' ? 'lg:grid-cols-3' : ''}`}>
          {/* Leaderboard */}
          <div className={activeTab === 'weekly' ? 'lg:col-span-2' : ''}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Rank
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      User
                    </th>
                    {activeTab === 'weekly' ? (
                      <>
                        {problems.map((problem) => (
                          <th key={problem.letter} className="px-3 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                            {problem.letter}
                          </th>
                        ))}
                      </>
                    ) : (
                      <>
                        <th className="px-6 py-3 text-center text-xs font-medium text-green-600 dark:text-green-400 uppercase tracking-wider">
                          Easy
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-yellow-600 dark:text-yellow-400 uppercase tracking-wider">
                          Medium
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-red-600 dark:text-red-400 uppercase tracking-wider">
                          Hard
                        </th>
                      </>
                    )}
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Score
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {activeTab === 'weekly' ? (
                    leaderboard.map((user) => (
                      <tr key={user.username} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-gray-600 font-medium">
                        <td className="px-6 py-4 whitespace-nowrap">
                          {user.rank}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Link
                            to={`/profile/${user.username}`}
                            className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer font-medium"
                          >
                            {user.username}
                          </Link>
                        </td>
                        {problems.map((problem) => (
                          <td key={problem.letter} className="px-3 py-4 whitespace-nowrap text-center">
                            <div className="flex justify-center">
                              <div className={`w-3 h-3 rounded-full ${
                                user.solutions[problem.letter] 
                                  ? 'bg-green-500' 
                                  : 'bg-gray-300 dark:bg-gray-600'
                              }`}></div>
                            </div>
                          </td>
                        ))}
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {user.totalScore}
                        </td>
                      </tr>
                    ))
                  ) : (
                    allTimeLeaderboard.map((user) => (
                      <tr key={user.username} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-gray-600 font-medium">
                        <td className="px-6 py-4 whitespace-nowrap">
                          {user.rank}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Link
                            to={`/profile/${user.username}`}
                            className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer font-medium"
                          >
                            {user.username}
                          </Link>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {user.easySolved}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {user.mediumSolved}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {user.hardSolved}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center">
                          {user.totalScore}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Problems List - Only show for Weekly tab */}
          {activeTab === 'weekly' && (
            <div className="lg:col-span-1">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 sticky top-8">
                <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    This Week's Problems
                  </h2>
                </div>
                <div className="p-6 space-y-4">
                  {problems.map((problem) => (
                    <div
                      key={problem.letter}
                      className="p-4 rounded-lg border border-gray-200 dark:border-gray-700"
                    >
                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center font-bold">
                          {problem.letter}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 dark:text-white">
                            {problem.title}
                          </div>
                          <div className={`text-sm font-medium mt-1 ${getDifficultyColor(problem.difficulty)}`}>
                            {problem.difficulty}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
  )
}

export default Home

