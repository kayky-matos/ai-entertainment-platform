import React, { useState } from 'react';
import { X } from 'lucide-react';  // Add X icon to imports
import {
  Twitter, MessageCircle, BookOpen, Film,
  Newspaper, MapPin, Star, Play
} from 'lucide-react';

interface Location {
  place: string;
  scenes: string[];
  facts: string[];
}

interface SocialSentiment {
  twitter: {
    positive: number;
    trending: boolean;
    recentTrend: string;
    topHashtags: string[];
  };
  reddit: {
    sentiment: number;
    activeCommunities: string[];
    mostDiscussedTopics: string[];
  };
}

interface FutureProjects {
  sequels: string;
  spinoffs: string;
  relatedProjects: string;
}

interface MovieDetails {
  title: string;
  year: number;
  duration: string;
  rating: number;
  ageRating: string;
  genre: string[];
  director: string;
  writer: string;
  cast: string[];
  synopsis: string;
  trailerUrl: string;
  posterImage: string;
  ratings: {
    imdb: string;
    rottenTomatoes: string;
    metacritic: string;
  };
  socialSentiment: SocialSentiment;
  funFacts: string[];
  behindTheScenes: string[];
  locations: Location[];
  futureProjects: FutureProjects;
  culturalImpact: string[];
  streamingOn: string[];
  userSentiment: number;
}

const EnhancedDetailsPage = () => {
  const [isPlaying, setIsPlaying] = useState(false);

  const movieDetails: MovieDetails = {
    title: "Inception",
    year: 2010,
    duration: "2h 28min",
    rating: 4.8,
    ageRating: "PG-13",
    genre: ["Action", "Sci-Fi", "Adventure"],
    director: "Christopher Nolan",
    writer: "Christopher Nolan",
    cast: ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
    synopsis: "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    trailerUrl: "https://www.youtube.com/embed/zJqESZktoYw",
    posterImage: "inception.jpg",
    ratings: {
      imdb: "8.8/10",
      rottenTomatoes: "87%",
      metacritic: "74/100"
    },
    socialSentiment: {
      twitter: {
        positive: 85,
        trending: true,
        recentTrend: "increasing",
        topHashtags: ["#Inception", "#Nolan", "#DreamHeist"]
      },
      reddit: {
        sentiment: 92,
        activeCommunities: ["r/movies", "r/inception", "r/ChristopherNolan"],
        mostDiscussedTopics: ["Dream Mechanics", "Ending Theories", "Score"]
      }
    },
    funFacts: [
      "The iconic 'BRRAAAHM' sound in the score has become a widely imitated trend in movie trailers",
      "The rotating hallway scene was achieved with a real rotating set, not CGI",
      "The entire film features no CGI blue or green screen shots",
      "Hans Zimmer's score was partly created from an extremely slowed down version of Édith Piaf's 'Non, je ne regrette rien'"
    ],
    behindTheScenes: [
      "Joseph Gordon-Levitt spent weeks learning to fight in a rotating set",
      "The cast had to attend lectures on dream theory and lucid dreaming",
      "The snow fortress scenes were filmed in real mountain locations"
    ],
    locations: [
      {
        place: "Los Angeles, USA",
        scenes: ["Opening sequences", "Dream training"],
        facts: ["Used real downtown locations", "Minimal set dressing required"]
      },
      {
        place: "Paris, France",
        scenes: ["Cafe scene", "Folding city"],
        facts: ["The folding Paris scene was mostly practical effects", "Shot on location in the Montmartre district"]
      },
      {
        place: "Tangier, Morocco",
        scenes: ["Market chase"],
        facts: ["Used local extras", "Real streets and markets"]
      }
    ],
    futureProjects: {
      sequels: "Inception 2 is coming soon",
      spinoffs: "Several video game adaptations were considered but not pursued",
      relatedProjects: "Nolan's 'Tenet' shares similar complex narrative structures"
    },
    culturalImpact: [
      "Popularized the concept of layered dream sequences in popular culture",
      "Influenced numerous subsequent films and TV shows",
      "Generated endless online discussions about its ending",
      "Led to increased interest in lucid dreaming"
    ],
    streamingOn: ["Netflix", "Amazon Prime"],
    userSentiment: 89
  };

  return (
    <div className="min-h-screen bg-[#13151a] text-white">
      {/* Hero Section */}
      <div className="h-[600px] relative bg-[#13151a]">
  {isPlaying ? (
    // Video Player
    <div className="relative w-full h-full">
      <iframe
        className="absolute top-0 left-0 w-full h-full"
        src="https://www.youtube.com/embed/Qwe6qXFTdgc?si=6f8yAhoPngZv7kMr"
        title="Inception Trailer"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowFullScreen
      />
      <div
        className="absolute top-4 right-4 z-30 cursor-pointer bg-black/50 p-2 rounded-full hover:bg-black/75 transition-colors"
        onClick={() => setIsPlaying(false)}
      >
        <X className="h-6 w-6 text-white" />
      </div>
    </div>
  ) : (
    // Poster with Play Button
    <div className="relative h-full">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#13151a]/60 to-[#13151a] z-10" />
      <img
        src="inception.jpg"
        alt="Inception Movie Poster"
        className="w-full h-full object-cover"
      />
      <button
        onClick={() => setIsPlaying(true)}
        className="absolute inset-0 w-full h-full flex items-center justify-center group z-20 hover:bg-black/30 transition-colors"
      >
        <div className="relative">
          <div className="absolute -inset-4 bg-white/10 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative h-20 w-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center border border-white/30 group-hover:bg-white/30 transition-colors">
            <Play className="h-10 w-10 text-white group-hover:scale-110 transition-transform" fill="white" />
          </div>
          <p className="absolute top-24 left-1/2 -translate-x-1/2 text-white text-lg font-medium opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
            Watch Trailer
          </p>
        </div>
      </button>
    </div>
  )}

  {/* Title and Info Overlay */}
  <div className="absolute bottom-0 left-0 right-0 z-20 pointer-events-none">
    <div className="max-w-7xl mx-auto px-8 py-12">
      <div className="space-y-4">
        <div className="text-sm text-gray-400 flex items-center gap-3">
          {movieDetails.genre.map((genre, index) => (
            <React.Fragment key={genre}>
              <span>{genre}</span>
              {index < movieDetails.genre.length - 1 && <span>•</span>}
            </React.Fragment>
          ))}
        </div>
        <h1 className="text-5xl font-bold">{movieDetails.title}</h1>
        <div className="flex items-center gap-4 text-lg text-gray-300">
          <span>{movieDetails.year}</span>
          <span>•</span>
          <span>{movieDetails.director}</span>
        </div>
      </div>
    </div>
  </div>
</div>

      <div className="max-w-7xl mx-auto px-8 py-12 space-y-16">
        {/* Ratings Section */}
        <div className="grid grid-cols-3 gap-8">
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">{movieDetails.ratings.imdb}</div>
            <div className="text-sm text-gray-400">IMDb</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-500">{movieDetails.ratings.rottenTomatoes}</div>
            <div className="text-sm text-gray-400">Rotten Tomatoes</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-500">{movieDetails.ratings.metacritic}</div>
            <div className="text-sm text-gray-400">Metacritic</div>
          </div>
        </div>

        {/* Social Sentiment Dashboard */}
        <div className="grid grid-cols-2 gap-8">
          <div className="bg-[#1a1d24] rounded-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <Twitter className="h-6 w-6 text-blue-400" />
              <h2 className="text-xl font-bold">Twitter Sentiment</h2>
            </div>
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Positive Reactions</span>
                <span className="text-2xl font-bold text-blue-400">{movieDetails.socialSentiment.twitter.positive}%</span>
              </div>
              <div>
                <h3 className="text-gray-400 mb-3">Trending Hashtags</h3>
                <div className="flex flex-wrap gap-2">
                  {movieDetails.socialSentiment.twitter.topHashtags.map((tag) => (
                    <span key={tag} className="px-3 py-1 bg-[#2a2d34] rounded-full text-sm text-blue-400">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-[#1a1d24] rounded-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <MessageCircle className="h-6 w-6 text-orange-500" />
              <h2 className="text-xl font-bold">Reddit Insights</h2>
            </div>
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Community Rating</span>
                <span className="text-2xl font-bold text-orange-500">{movieDetails.socialSentiment.reddit.sentiment}%</span>
              </div>
              <div>
                <h3 className="text-gray-400 mb-3">Active Communities</h3>
                <div className="flex flex-wrap gap-2">
                  {movieDetails.socialSentiment.reddit.activeCommunities.map((community) => (
                    <span key={community} className="px-3 py-1 bg-[#2a2d34] rounded-full text-sm text-orange-500">
                      {community}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Content Sections */}
        <div className="grid grid-cols-3 gap-8">
          {/* Main Content - 2 columns */}
          <div className="col-span-2 space-y-8">
            {/* Synopsis */}
            <section className="bg-[#1a1d24] rounded-lg p-8">
              <div className="flex items-center gap-3 mb-6">
                <BookOpen className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold">Synopsis</h2>
              </div>
              <p className="text-gray-300 leading-relaxed">{movieDetails.synopsis}</p>
            </section>

            {/* Behind the Scenes */}
            <section className="bg-[#1a1d24] rounded-lg p-8">
              <div className="flex items-center gap-3 mb-6">
                <Film className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold">Behind the Scenes</h2>
              </div>
              <div className="space-y-4">
                {movieDetails.behindTheScenes.map((fact, index) => (
                  <div key={index} className="flex gap-3 text-gray-300">
                    <span className="text-purple-500">•</span>
                    <p>{fact}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* Fun Facts */}
            <section className="bg-[#1a1d24] rounded-lg p-8">
              <div className="flex items-center gap-3 mb-6">
                <BookOpen className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold">Fun Facts</h2>
              </div>
              <div className="space-y-4">
                {movieDetails.funFacts.map((fact, index) => (
                  <div key={index} className="flex gap-3 text-gray-300">
                    <span className="text-purple-500">•</span>
                    <p>{fact}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* Filming Locations */}
            <section className="bg-[#1a1d24] rounded-lg p-8">
              <div className="flex items-center gap-3 mb-6">
                <MapPin className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold">Filming Locations</h2>
              </div>
              <div className="space-y-6">
                {movieDetails.locations.map((location) => (
                  <div key={location.place} className="space-y-3">
                    <h3 className="text-lg font-semibold">{location.place}</h3>
                    <div className="pl-4 space-y-2 text-gray-300">
                      <p>
                        <span className="text-gray-400">Scenes: </span>
                        {location.scenes.join(', ')}
                      </p>
                      {location.facts.map((fact, index) => (
                        <div key={index} className="flex gap-3">
                          <span className="text-purple-500">•</span>
                          <p>{fact}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Cultural Impact */}
            <section className="bg-[#1a1d24] rounded-lg p-8">
              <div className="flex items-center gap-3 mb-6">
                <Newspaper className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold">Cultural Impact</h2>
              </div>
              <div className="space-y-4">
                {movieDetails.culturalImpact.map((impact, index) => (
                  <div key={index} className="flex gap-3 text-gray-300">
                    <span className="text-purple-500">•</span>
                    <p>{impact}</p>
                  </div>
                ))}
              </div>
            </section>
          </div>

          {/* Sidebar Content - 1 column */}
          <div className="space-y-8">
            {/* Cast */}
            <div className="bg-[#1a1d24] rounded-lg p-8">
              <h2 className="text-xl font-bold mb-6">Cast & Crew</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-gray-400 mb-2">Director</p>
                  <p className="text-gray-300">{movieDetails.director}</p>
                </div>
                <div>
                  <p className="text-gray-400 mb-2">Cast</p>
                  <div className="space-y-2">
                    {movieDetails.cast.map((actor) => (
                      <p key={actor} className="text-gray-300">{actor}</p>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Content Warning & Age Rating */}
            <div className="bg-[#1a1d24] rounded-lg p-8">
              <h2 className="text-xl font-bold mb-6">Content Advisory</h2>
              <div className="space-y-4 text-gray-300">
                <p><span className="text-gray-400">Age Rating: </span>{movieDetails.ageRating}</p>
                <p><span className="text-gray-400">Warnings: </span>Photosensitive violence</p>
              </div>
            </div>

            {/* Streaming Availability */}
            <div className="bg-[#1a1d24] rounded-lg p-8">
              <h2 className="text-xl font-bold mb-6">Available on</h2>
              <div className="flex flex-wrap gap-2">
                {movieDetails.streamingOn.map((platform) => (
                  <span key={platform} className="px-3 py-1 bg-[#2a2d34] rounded-full text-sm text-gray-300">
                    {platform}
                  </span>
                ))}
              </div>
            </div>

            {/* Future Projects */}
            <div className="bg-[#1a1d24] rounded-lg p-8">
              <h2 className="text-xl font-bold mb-6">Future Projects</h2>
              <div className="space-y-4 text-gray-300">
                <p><span className="text-gray-400">Sequels: </span>{movieDetails.futureProjects.sequels}</p>
                <p><span className="text-gray-400">Spin-offs: </span>{movieDetails.futureProjects.spinoffs}</p>
                <p><span className="text-gray-400">Related: </span>{movieDetails.futureProjects.relatedProjects}</p>
              </div>
            </div>

            {/* User Sentiment */}
            <div className="bg-[#1a1d24] rounded-lg p-8">
              <h2 className="text-xl font-bold mb-6">User Sentiment</h2>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Overall Rating</span>
                <span className="text-2xl font-bold text-purple-500">{movieDetails.userSentiment}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDetailsPage;