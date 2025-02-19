// components/browse-page.tsx
import React, { useState } from 'react';
import { Film, Tv2, TrendingUp } from 'lucide-react';

const BrowsePage = () => {
  const [activeFilter, setActiveFilter] = useState('all');

  const categories = [
    {
      id: 'movies',
      label: 'Movies',
      icon: <Film className="w-5 h-5 mr-2" />,
      description: 'Discover great movies with detailed insights'
    },
    {
      id: 'tv',
      label: 'TV Series',
      icon: <Tv2 className="w-5 h-5 mr-2" />,
      description: 'Explore trending series and get suggestions'
    },
    {
      id: 'trending',
      label: 'Trending',
      icon: <TrendingUp className="w-5 h-5 mr-2" />,
      description: 'Stay updated with what\'s popular'
    }
  ];

  const content = [
    {
      id: 1,
      title: 'The Shawshank Redemption',
      type: 'movie',
      year: 1994,
      rating: 4.9,
      genre: 'Drama',
      image: 'shawshank-redemption.jpg'
    },
    {
      id: 2,
      title: 'Breaking Bad',
      type: 'series',
      year: 2008,
      rating: 4.9,
      genre: 'Drama',
      image: 'breaking-bad.jpg'
    }
  ];

  return (
    <div className="min-h-screen bg-[#13151a] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Browse Movies & Series</h1>

        {/* Category Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {categories.map((category) => (
            <div
              key={category.id}
              className="bg-[#1a1d24] hover:bg-[#2a2d34] transition-colors rounded-lg p-6 border border-gray-800"
            >
              <div className="flex items-center text-white mb-2">
                {category.icon}
                <h3 className="text-lg font-semibold">{category.label}</h3>
              </div>
              <p className="text-gray-400 text-sm">{category.description}</p>
            </div>
          ))}
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {content.map((item) => (
            <div
              key={item.id}
              className="bg-[#1a1d24] overflow-hidden rounded-lg border border-gray-800 group hover:bg-[#2a2d34] transition-colors"
            >
              <div className="relative">
                <img
                  src={item.image}
                  alt={item.title}
                  className="w-full h-64 object-cover"
                />
                <div className="absolute top-2 right-2 bg-black/70 px-2 py-1 rounded text-sm">
                  {item.type === 'movie' ? 'Movie' : 'TV Series'}
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
                <div className="flex items-center justify-between text-gray-400">
                  <div className="flex items-center space-x-2">
                    <span>{item.year}</span>
                    <span>•</span>
                    <span>{item.genre}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-yellow-400">★</span>
                    <span className="ml-1">{item.rating}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BrowsePage;