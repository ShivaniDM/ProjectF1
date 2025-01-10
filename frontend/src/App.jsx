import F1Dashboard from './components/F1Dashboard'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-gray-900 text-white py-6 mb-6">
        <div className="max-w-[1200px] mx-auto px-5">
          <h1 className="text-2xl font-bold">Formula 1 - 2024 Season Results</h1>
        </div>
      </header>
      <main>
        <F1Dashboard />
      </main>
    </div>
  )
}

export default App