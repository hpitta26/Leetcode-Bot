function Banner() {
  return (
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
  )
}

export default Banner

