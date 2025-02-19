// components/trending-page.tsx
import React, { useState } from 'react';
import { Search, Play, Globe, Star, TrendingUp, ThumbsUp } from 'lucide-react';

const TrendingPage = () => {
  const [selectedPlatform, setSelectedPlatform] = useState('all');

  const streamingPlatforms = [
    { id: 'all', name: 'All Platforms' },
    { id: 'netflix', name: 'Netflix' },
    { id: 'prime', name: 'Prime Video' },
    { id: 'disney', name: 'Disney+' },
    { id: 'hulu', name: 'Hulu' },
    { id: 'hbo', name: 'HBO Max' },
    { id: 'viki', name: 'Viki' }
  ];

  const trendingContent = [
    {
      id: 1,
      title: 'The Matrix',
      platforms: ['netflix', 'prime'],
      image: 'matrix.jpeg',
      rating: {
        imdb: '8.8/10',
        rottenTomatoes: '87%',
        metacritic: '74/100'
      },
      userSentiment: 92,
      year: 1999,
      director: 'Lana Wachowski',
      genres: ['Sci-Fi', 'Action', 'Thriller'],
      availability: 'Global',
      contentWarning: 'intense sci-fi violence'
    },
    {
      id: 2,
      title: 'Moving',
      platforms: ['hulu', 'disney', 'viki'],
      image: 'moving.jpg',
      rating: {
        imdb: '8.7/10',
        rottenTomatoes: '92%',
        metacritic: '85/100'
      },
      userSentiment: 95,
      year: 2023,
      director: 'Park In-je',
      genres: ['Action', 'Sci-Fi', 'Drama'],
      availability: 'Global',
      contentWarning: 'action violence'
    },
    {
      id: 3,
      title: 'The Glory',
      platforms: ['netflix', 'viki'],
      image: 'the-glory.jpg',
      rating: {
        imdb: '8.1/10',
        rottenTomatoes: '95%',
        metacritic: '82/100'
      },
      userSentiment: 89,
      year: 2022,
      director: 'Ahn Gil-ho',
      genres: ['Drama', 'Thriller', 'Mystery'],
      availability: 'All Regions',
      contentWarning: 'mature themes'
    },
    {
      id: 4,
      title: 'Mr. Queen',
      platforms: ['viki'],
      image: 'mr-queen.jpg',
      rating: {
        imdb: '8.8/10',
        rottenTomatoes: '94%',
        metacritic: '83/100'
      },
      userSentiment: 96,
      year: 2020,
      director: 'Yoon Sung-sik',
      genres: ['Comedy', 'Historical', 'Romance'],
      availability: 'All Regions',
      contentWarning: 'mild violence and suggestive content'
    },
    {
      id: 5,
      title: 'The Mandalorian',
      platforms: ['disney'],
      image: 'mandalorian.jpg',
      rating: {
        imdb: '8.7/10',
        rottenTomatoes: '93%',
        metacritic: '76/100'
      },
      userSentiment: 91,
      year: 2019,
      director: 'Jon Favreau',
      genres: ['Sci-Fi', 'Action', 'Adventure'],
      availability: 'All Regions',
      contentWarning: 'sci-fi action violence'
    },
    {
      id: 6,
      title: 'Extraordinary Attorney Woo',
      platforms: ['netflix', 'viki'],
      image: 'attorney-woo.jpg',
      rating: {
        imdb: '8.7/10',
        rottenTomatoes: '96%',
        metacritic: '85/100'
      },
      userSentiment: 97,
      year: 2022,
      director: 'Yoo In-sik',
      genres: ['Drama', 'Legal', 'Romance'],
      availability: 'Global',
      contentWarning: 'mild themes'
    },
    {
      id: 7,
      title: 'Strong Girl Nam-soon',
      platforms: ['netflix', 'viki'],
      image: 'strong-girl-namsoon.jpg',
      rating: {
        imdb: '8.2/10',
        rottenTomatoes: '91%',
        metacritic: '79/100'
      },
      userSentiment: 88,
      year: 2023,
      director: 'Kim Jung-sik',
      genres: ['Action', 'Comedy', 'Crime'],
      availability: 'Global',
      contentWarning: 'action violence and drug references'
    },
    {
      id: 8,
      title: 'Daily Dose of Sunshine',
      platforms: ['netflix', 'viki'],
      image: 'daily-dose-sunshine.jpg',
      rating: {
        imdb: '8.4/10',
        rottenTomatoes: '92%',
        metacritic: '81/100'
      },
      userSentiment: 94,
      year: 2023,
      director: 'Lee Jae-gyu',
      genres: ['Drama', 'Medical', 'Slice of Life'],
      availability: 'Global',
      contentWarning: 'medical themes and emotional content'
    }
  ];

  const filteredContent = selectedPlatform === 'all'
    ? trendingContent
    : trendingContent.filter(item => item.platforms.includes(selectedPlatform));

  return (
    <div className="min-h-screen bg-[#13151a] text-white">
      <div className="max-w-7xl mx-auto p-8 space-y-8">
        {/* Header and filters remain the same */}
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Trending Now</h1>
          <p className="text-gray-400">Stay updated with what's popular across all platforms</p>
        </div>

        {/* Search and Platform Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="relative">
            <Search className="absolute left-4 top-3.5 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search trending content..."
              className="w-full bg-[#1a1d24] text-white pl-12 pr-4 py-3 rounded-lg border border-gray-700 focus:border-purple-500 focus:outline-none"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            {streamingPlatforms.map((platform) => (
              <button
                key={platform.id}
                onClick={() => setSelectedPlatform(platform.id)}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  selectedPlatform === platform.id
                    ? 'bg-purple-500 text-white'
                    : 'bg-[#1a1d24] text-gray-400 hover:bg-[#2a2d34]'
                }`}
              >
                {platform.name}
              </button>
            ))}
          </div>
        </div>

        {/* Content Grid */}
        <div className="space-y-8">
          {filteredContent.map((item) => (
            <div key={item.id} className="bg-[#1a1d24] rounded-lg overflow-hidden border border-gray-800">
              <div className="relative">
                <img
                  src={item.image}
                  alt={item.title}
                  className="w-full h-[400px] object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#1a1d24] via-transparent to-transparent">
                  <div className="absolute bottom-0 left-0 p-8">
                    <h2 className="text-4xl font-bold text-white mb-2">{item.title}</h2>
                    <div className="flex items-center space-x-4 text-sm text-gray-300">
                      <span>{item.year}</span>
                      <span>•</span>
                      <span>{item.director}</span>
                    </div>
                    <div className="flex items-center space-x-2 mt-2">
                      {item.genres.map((genre) => (
                        <span key={genre} className="px-2 py-1 bg-[#2a2d34] rounded text-xs text-gray-300">
                          {genre}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-8 space-y-6">
                {/* Ratings */}
                <div className="grid grid-cols-3 gap-8">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-400">{item.rating.imdb}</div>
                    <div className="text-sm text-gray-400">IMDb</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-500">{item.rating.rottenTomatoes}</div>
                    <div className="text-sm text-gray-400">Rotten Tomatoes</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-500">{item.rating.metacritic}</div>
                    <div className="text-sm text-gray-400">Metacritic</div>
                  </div>
                </div>

                {/* Content Warning */}
                <div className="bg-[#2a2d34] rounded-lg p-4">
                  <div className="flex items-center space-x-2 text-red-400 text-sm">
                    <span className="font-medium">Content Warning:</span>
                    <span>{item.contentWarning}</span>
                  </div>
                </div>

                {/* Streaming Availability */}
                <div>
                  <div className="text-sm text-gray-300 mb-2">Available on:</div>
                  <div className="flex space-x-4">
                    {item.platforms.map((platform) => (
                      <div key={platform} className="px-3 py-1 bg-[#2a2d34] rounded text-sm text-gray-300">
                        {streamingPlatforms.find(p => p.id === platform)?.name}
                      </div>
                    ))}
                  </div>
                </div>

                {/* User Sentiment */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 px-3 py-1 bg-[#2a2d34] rounded">
                    <span className="text-sm text-gray-300">User Sentiment</span>
                    <span className="text-sm text-purple-500">{item.userSentiment}%</span>
                  </div>
                  {/* Watch Now Button */}
                  <button className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors flex items-center space-x-2">
                    <Play className="h-5 w-5" />
                    <span>Watch Now</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TrendingPage;