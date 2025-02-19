// App.tsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useState } from 'react';
import { Search, Film, Tv2, TrendingUp, Heart, Bookmark, Home, Settings, X, Menu } from 'lucide-react';
import { useTranslation } from './hooks/useTranslation';
import { LanguageSelector } from './components/LanguageSelector';
import ChatbotTrigger from './components/ChatbotTrigger';
import BrowsePage from './components/browse-page';
import WatchlistPage from './components/watchlist-page';
import TrendingPage from './components/trending-page';
import EnhancedDetailsPage from './components/enhanced-details-page';

function CategoryCard({ icon: Icon, title, description }: { icon: any, title: string, description: string }) {
  return (
    <div className="bg-[#1a1d24] p-6 rounded-lg hover:bg-[#2a2d34] transition-colors cursor-pointer">
      <div className="flex items-center space-x-4 mb-2">
        <Icon className="w-6 h-6 text-gray-400" />
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>
      <p className="text-gray-400 text-sm">{description}</p>
    </div>
  );
}

function SearchBar({ t }: { t: any }) {
  return (
    <div className="relative mb-12">
      <Search className="absolute left-4 top-3.5 h-5 w-5 text-gray-400" />
      <input
        type="text"
        placeholder={t('searchPlaceholder')}
        className="w-full bg-[#1a1d24] text-white pl-12 pr-4 py-3 rounded-lg border border-gray-700 focus:border-purple-500 focus:outline-none"
      />
    </div>
  );
}

import { useNavigate } from 'react-router-dom';

function MovieDetails({ t }: { t: any }) {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate('/details/inception');
  };
  return (
    <div className="bg-[#1a1d24] rounded-lg overflow-hidden mt-12">
      <div className="relative">
        <img
          src="inception.jpg"
          alt="Inception movie scene"
          className="w-full h-[400px] object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#1a1d24] to-transparent">
          <div className="absolute bottom-0 left-0 right-0 p-8">
            <h2 className="text-4xl font-bold text-white mb-2">Inception</h2>
            <div className="flex items-center space-x-4 text-sm text-gray-300">
              <span>2010</span>
              <span>•</span>
              <span>Christopher Nolan</span>
            </div>
            <div className="flex items-center space-x-2 mt-2">
              <span className="px-2 py-1 bg-[#2a2d34] rounded text-xs text-gray-300">SCI-FI</span>
              <span className="px-2 py-1 bg-[#2a2d34] rounded text-xs text-gray-300">Action</span>
              <span className="px-2 py-1 bg-[#2a2d34] rounded text-xs text-gray-300">Thriller</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-8 space-y-8">
        <div className="grid grid-cols-3 gap-8">
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">8.8/10</div>
            <div className="text-sm text-gray-400">IMDb</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-500">87%</div>
            <div className="text-sm text-gray-400">Rotten Tomatoes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-500">74/100</div>
            <div className="text-sm text-gray-400">Metacritic</div>
          </div>
        </div>

        <div className="bg-[#2a2d34] rounded-lg p-4">
          <div className="flex items-center space-x-2 text-red-400 text-sm">
            <span className="font-medium">{t('contentWarning')}</span>
            <span>photosensitive violence</span>
          </div>
        </div>

        <div>
          <div className="text-sm text-gray-300 mb-2">{t('availableOn')}</div>
          <div className="flex space-x-4">
            <div className="px-3 py-1 bg-[#2a2d34] rounded text-sm text-gray-300">Netflix</div>
            <div className="px-3 py-1 bg-[#2a2d34] rounded text-sm text-gray-300">Amazon Prime</div>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 px-3 py-1 bg-[#2a2d34] rounded">
            <span className="text-sm text-gray-300">{t('userSentiment')}</span>
            <span className="text-sm text-purple-500">89%</span>
          </div>
            <button
    onClick={handleViewDetails}
    className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors"
  >
    View Details
  </button>
        </div>
      </div>
    </div>
  );
}

function Header({ onMenuClick, t, currentLanguage, setLanguage, availableLanguages }: {
  onMenuClick: () => void,
  t: any,
  currentLanguage: string,
  setLanguage: (lang: string) => void,
  availableLanguages: { code: string, name: string }[]
}) {
  return (
    <div className="flex justify-between items-center mb-8">
      <button
        className="w-8 h-8 flex items-center justify-center rounded-full bg-[#2a2d34] text-gray-400 hover:text-white"
        onClick={onMenuClick}
      >
        <Menu size={16} />
      </button>

      <h1 className="text-2xl font-bold text-purple-500">entertainment.ai</h1>

      <div className="flex items-center space-x-4">
        <LanguageSelector
          currentLanguage={currentLanguage}
          languages={availableLanguages}
          onLanguageChange={setLanguage}
        />
        <ChatbotTrigger t={t} />
        <button className="w-8 h-8 flex items-center justify-center rounded-full bg-purple-500 text-white">
          <span className="text-sm">P</span>
        </button>
        <button className="w-8 h-8 flex items-center justify-center rounded-full bg-[#2a2d34] text-gray-400 hover:text-white">
          <Settings size={16} />
        </button>
        <button className="w-8 h-8 flex items-center justify-center rounded-full bg-[#2a2d34] text-gray-400 hover:text-white">
          <Heart size={16} />
        </button>
        <button className="w-8 h-8 flex items-center justify-center rounded-full bg-[#2a2d34] text-gray-400 hover:text-white">
          <Bookmark size={16} />
        </button>
      </div>
    </div>
  );
}

function Sidebar({ isOpen, onClose, t }: { isOpen: boolean, onClose: () => void, t: any }) {
  return (
    <div className={`fixed left-0 top-0 h-full w-64 bg-[#1a1d24] p-6 border-r border-gray-800 transform transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full'} z-50`}>
      <div className="flex items-center justify-between mb-10">
        <h1 className="text-2xl font-bold text-purple-500">entertainment.ai</h1>
        <button className="text-gray-400 hover:text-white" onClick={onClose}>
          <X size={20} />
        </button>
      </div>

      <nav className="space-y-4">
        <Link to="/" className="flex items-center space-x-3 text-gray-300 hover:text-white p-2 rounded hover:bg-gray-800">
          <Home size={20} />
          <span>{t('home')}</span>
        </Link>
        <Link to="/browse" className="flex items-center space-x-3 text-gray-300 hover:text-white p-2 rounded hover:bg-gray-800">
          <Film size={20} />
          <span>{t('moviesAndSeries')}</span>
        </Link>
        <Link to="/trending" className="flex items-center space-x-3 text-gray-300 hover:text-white p-2 rounded hover:bg-gray-800">
          <TrendingUp size={20} />
          <span>{t('trending')}</span>
        </Link>
        <Link to="/watchlist" className="flex items-center space-x-3 text-gray-300 hover:text-white p-2 rounded hover:bg-gray-800">
          <Bookmark size={20} />
          <span>{t('watchlist')}</span>
        </Link>
      </nav>
    </div>
  );
}

function HomePage({ t }: { t: any }) {
  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold text-white mb-2">{t('discover')}</h1>
      <p className="text-gray-400 mb-8">{t('explore')}</p>

      <SearchBar t={t} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <CategoryCard
          icon={Film}
          title={t('movies')}
          description={t('moviesDescription')}
        />
        <CategoryCard
          icon={Tv2}
          title={t('tvSeries')}
          description={t('tvSeriesDescription')}
        />
        <CategoryCard
          icon={TrendingUp}
          title={t('trending')}
          description={t('trendingDescription')}
        />
      </div>

      <MovieDetails t={t} />
    </div>
  );
}

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { t, currentLanguage, setLanguage, availableLanguages } = useTranslation();

  return (
    <Router>
      <div className="min-h-screen bg-[#13151a] text-white">
        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} t={t} />
        <div className="p-8">
          <Header
            onMenuClick={() => setIsSidebarOpen(true)}
            t={t}
            currentLanguage={currentLanguage}
            setLanguage={setLanguage}
            availableLanguages={availableLanguages}
          />

          <Routes>
            <Route path="/" element={<HomePage t={t} />} />
            <Route path="/browse" element={<BrowsePage />} />
            <Route path="/trending" element={<TrendingPage />} />
            <Route path="/watchlist" element={<WatchlistPage />} />
            <Route path="/details/:id" element={<EnhancedDetailsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;