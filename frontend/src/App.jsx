import { useState, useEffect } from 'react'

function App() {
  const [competition, setCompetition] = useState(null)
  const [problems, setProblems] = useState([])
  const [leaderboard, setLeaderboard] = useState([])
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
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Scrolling Banner */}
      <div className="relative overflow-hidden bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 text-white py-1 lg:py-2.5">
        <div className="flex animate-scroll-seamless hover:[animation-play-state:paused] whitespace-nowrap">
          {[...Array(20)].map((_, i) => (
            <div key={i} className="inline-flex items-center shrink-0">
              <span className="text-base lg:text-lg font-semibold px-4">
                Time Left: 2 days 14 hours 23 minutes
              </span>
              <span className="flex-shrink-0">
                <svg 
                  className="w-5 h-5 animate-spin-slow" 
                  viewBox="0 0 200 200" 
                  fill="none" 
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path 
                    d="M100.5 3L114.058 58.7724L157.809 21.6208L135.996 74.7109L193.228 70.3708L144.375 100.5L193.228 130.629L135.996 126.289L157.809 179.379L114.058 142.228L100.5 198L86.9419 142.228L43.1909 179.379L65.0044 126.289L7.77197 130.629L56.625 100.5L7.77197 70.3708L65.0044 74.7109L43.1909 21.6208L86.9419 58.7724L100.5 3Z" 
                    fill="currentColor"
                  />
                </svg>
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Main Header */}
      <header>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            Reach TIP Leaderboard
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Leaderboard */}
          <div className="lg:col-span-2">
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
                    {problems.map((problem) => (
                      <th key={problem.letter} className="px-3 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        {problem.letter}
                      </th>
                    ))}
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Score
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {leaderboard.map((user) => (
                    <tr key={user.username} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {user.rank}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          {user.username}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {user.problemsSolved} solved
                        </div>
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
                        <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                          {user.totalScore}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Problems List */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 sticky top-8">
              <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Problems
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
        </div>
      </main>
      </div>
  )
}

export default App
