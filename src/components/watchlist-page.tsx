// components/watchlist-page.tsx
import React, { useState } from 'react';
import { Trash2, Clock, Check, Play, Star } from 'lucide-react';

const WatchlistPage = () => {
  const [filter, setFilter] = useState('all');

  const filters = [
    { id: 'all', label: 'All' },
    { id: 'unwatched', label: 'Unwatched' },
    { id: 'watching', label: 'In Progress' },
    { id: 'completed', label: 'Completed' }
  ];

  const watchlist = [
    {
      id: 1,
      title: 'The Last of Us',
      type: 'series',
      image: 'the-last-of-us.jpg',
      status: 'watching',
      progress: '4/10 Episodes',
      rating: 4.9,
      addedDate: '2024-02-10'
    },
    {
      id: 2,
      title: 'Dune',
      type: 'movie',
      image: 'dune.jpg',
      status: 'unwatched',
      rating: 4.8,
      addedDate: '2024-02-08'
    },
    {
      id: 3,
      title: 'Breaking Bad',
      type: 'series',
      image: 'breaking-bad.jpg',
      status: 'completed',
      rating: 4.9,
      addedDate: '2024-01-15'
    }
  ];

  const filteredWatchlist = filter === 'all' 
    ? watchlist 
    : watchlist.filter(item => item.status === filter);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'unwatched':
        return <Clock className="h-5 w-5 text-gray-400" />;
      case 'watching':
        return <Play className="h-5 w-5 text-purple-500" />;
      case 'completed':
        return <Check className="h-5 w-5 text-green-400" />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#13151a] text-white">
      <div className="max-w-7xl mx-auto p-8 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">My Watchlist</h1>
          <p className="text-gray-400">Keep track of what you want to watch</p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          {filters.map((filterOption) => (
            <button
              key={filterOption.id}
              onClick={() => setFilter(filterOption.id)}
              className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                filter === filterOption.id
                  ? 'bg-purple-500 text-white'
                  : 'bg-[#1a1d24] text-gray-400 hover:bg-[#2a2d34]'
              }`}
            >
              {filterOption.label}
            </button>
          ))}
        </div>

        {/* Watchlist Grid */}
        {filteredWatchlist.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredWatchlist.map((item) => (
              <div 
                key={item.id} 
                className="bg-[#1a1d24] rounded-lg overflow-hidden group hover:bg-[#2a2d34] transition-colors border border-gray-800"
              >
                <div className="relative">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-64 object-cover"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3">
                    <button className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
                      View Details
                    </button>
                    <button className="p-2 bg-red-900/50 text-red-400 rounded-lg hover:bg-red-900/70 transition-colors">
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                  <div className="absolute top-2 right-2 bg-black/70 px-2 py-1 rounded text-white text-sm">
                    {item.type === 'movie' ? 'Movie' : 'TV Series'}
                  </div>
                </div>
                <div className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-lg text-white">{item.title}</h3>
                    {getStatusIcon(item.status)}
                  </div>
                  <div className="space-y-2">
                    {item.progress && (
                      <div className="text-sm text-gray-400">
                        Progress: {item.progress}
                      </div>
                    )}
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center">
                        <Star className="h-4 w-4 text-yellow-400 mr-1" />
                        <span className="text-white">{item.rating}</span>
                      </div>
                      <span className="text-gray-400">
                        Added {new Date(item.addedDate).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-[#1a1d24] border border-gray-800 rounded-lg p-4 text-gray-400">
            No items found in your watchlist for the selected filter.
          </div>
        )}
      </div>
    </div>
  );
};

export default WatchlistPage;