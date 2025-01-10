import { useState, useEffect } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const F1Dashboard = () => {
  const [raceResults, setRaceResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null); // Reset error state
        
        const response = await axios.get(`${BASE_URL}/api/standings`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        setRaceResults(response.data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.response?.data?.detail || err.message || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-5 text-center bg-white rounded-lg shadow m-5">
        <div className="animate-pulse">Loading race results...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-5 text-center bg-white rounded-lg shadow m-5 text-red-500">
        <h3 className="font-bold mb-2">Error Loading Data</h3>
        <p>{error}</p>
        <button 
          onClick={() => window.location.reload()}
          className="mt-3 px-4 py-2 bg-gray-100 rounded hover:bg-gray-200 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-5 max-w-[1200px] mx-auto">
      <h2 className="text-2xl font-bold mb-5 text-gray-800">F1 2024 Race Results</h2>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="p-4 text-left font-medium text-gray-700 border-b">Grand Prix</th>
                <th className="p-4 text-left font-medium text-gray-700 border-b">Date</th>
                <th className="p-4 text-left font-medium text-gray-700 border-b">Winner</th>
                <th className="p-4 text-left font-medium text-gray-700 border-b">Car</th>
                <th className="p-4 text-left font-medium text-gray-700 border-b">Laps</th>
                <th className="p-4 text-left font-medium text-gray-700 border-b">Time</th>
              </tr>
            </thead>
            <tbody>
              {raceResults.map((race, index) => (
                <tr 
                  key={index}
                  className={`hover:bg-gray-50 transition-colors ${
                    index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                  }`}
                >
                  <td className="p-4 border-b">{race['Grand Prix']}</td>
                  <td className="p-4 border-b">{race.Date}</td>
                  <td className="p-4 border-b">
                    <span 
                      className={`inline-block px-3 py-1 rounded text-white text-sm ${
                        race.Winner?.includes('VER') ? 'bg-[#0600EF]' :
                        race.Winner?.includes('LEC') ? 'bg-[#DC0000]' :
                        race.Winner?.includes('NOR') ? 'bg-[#FF8700]' :
                        race.Winner?.includes('SAI') ? 'bg-[#DC0000]' : 'bg-gray-600'
                      }`}
                    >
                      {race.Winner?.replace(/([A-Z]{3})$/, ' $1')}
                    </span>
                  </td>
                  <td className="p-4 border-b">{race.Car}</td>
                  <td className="p-4 border-b">{race.Laps}</td>
                  <td className="p-4 border-b">{race.Time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default F1Dashboard;