import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader, Globe, Star, Minimize, Maximize, X } from 'lucide-react';

// Simplified Card components
const Card = ({ className = "", children, ...props }) => (
  <div className={`rounded-lg border bg-card text-card-foreground shadow-sm ${className}`} {...props}>
    {children}
  </div>
);

const CardContent = ({ className = "", children, ...props }) => (
  <div className={`p-6 pt-0 ${className}`} {...props}>
    {children}
  </div>
);

const FloatingRAGChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [currentRating, setCurrentRating] = useState({ title: '', rating: 0, review: '' });
  const [isMinimized, setIsMinimized] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [position, setPosition] = useState({ x: 'auto', y: 'auto' });
  const [dimensions, setDimensions] = useState({ width: 500, height: 700 });
  const [resizeDirection, setResizeDirection] = useState(null);
  const dragRef = useRef(null);
  const resizeRef = useRef(null);
  const messagesEndRef = useRef(null);
  const startResizePos = useRef(null);
  const startDimensions = useRef(null);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
    { code: 'de', name: 'Deutsch' },
    { code: 'it', name: 'Italiano' },
    { code: 'pt', name: 'Português' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'hi', name: 'Hindi' }
  ];

  // Content moderation
  const moderateContent = (text) => {
    const sensitiveTerms = [
      'insult', 'violence', 'porn', 'explicit', 'kill',
    ];
    const containsSensitiveContent = sensitiveTerms.some(term =>
      text.toLowerCase().includes(term)
    );
    return {
      isAppropriate: !containsSensitiveContent,
      message: containsSensitiveContent ?
        "Your review contains inappropriate content. Please revise it." :
        "Review accepted"
    };
  };

  // Window dragging
  useEffect(() => {
    const handleDrag = (e) => {
      if (isDragging && dragRef.current) {
        setPosition({
          x: e.clientX - dragRef.current.offsetWidth / 2,
          y: e.clientY - 20
        });
      }
    };

    const handleDragEnd = () => {
      setIsDragging(false);
    };

    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', handleDragEnd);

    return () => {
      document.removeEventListener('mousemove', handleDrag);
      document.removeEventListener('mouseup', handleDragEnd);
    };
  }, [isDragging]);

  // Window resizing
  useEffect(() => {
    const handleResize = (e) => {
      if (isResizing && resizeRef.current && startResizePos.current && startDimensions.current) {
        e.preventDefault();

        const deltaX = e.clientX - startResizePos.current.x;
        const deltaY = e.clientY - startResizePos.current.y;

        let newWidth = startDimensions.current.width;
        let newHeight = startDimensions.current.height;

        if (resizeDirection.includes('e')) {
          newWidth = Math.max(400, startDimensions.current.width + deltaX);
        }
        if (resizeDirection.includes('s')) {
          newHeight = Math.max(500, startDimensions.current.height + deltaY);
        }

        setDimensions({ width: newWidth, height: newHeight });
      }
    };

    const handleResizeEnd = () => {
      setIsResizing(false);
      setResizeDirection(null);
      startResizePos.current = null;
      startDimensions.current = null;
    };

    document.addEventListener('mousemove', handleResize);
    document.addEventListener('mouseup', handleResizeEnd);

    return () => {
      document.removeEventListener('mousemove', handleResize);
      document.removeEventListener('mouseup', handleResizeEnd);
    };
  }, [isResizing, resizeDirection]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startResize = (e, direction) => {
    e.preventDefault();
    setIsResizing(true);
    setResizeDirection(direction);
    startResizePos.current = { x: e.clientX, y: e.clientY };
    startDimensions.current = { ...dimensions };
  };

  const handleRatingSubmit = async () => {
    const moderationResult = moderateContent(currentRating.review);
    if (!moderationResult.isAppropriate) {
      setMessages(prev => [...prev, {
        type: 'bot',
        content: moderationResult.message,
        timestamp: new Date(),
        isError: true
      }]);
      return;
    }
    setMessages(prev => [...prev, {
      type: 'bot',
      content: `Thank you for rating "${currentRating.title}" with ${currentRating.rating} stars!`,
      timestamp: new Date()
    }]);
    setShowRatingModal(false);
    setCurrentRating({ title: '', rating: 0, review: '' });
  };

  const RatingModal = () => (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
      <Card className="w-full max-w-md m-4 bg-gray-900 border-gray-700">
        <CardContent className="p-6 space-y-4">
          <h3 className="text-xl font-bold text-white">Rate & Review</h3>
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Movie/Show Title"
              value={currentRating.title}
              onChange={(e) => setCurrentRating(prev => ({ ...prev, title: e.target.value }))}
              className="w-full px-4 py-2 bg-gray-800 border-gray-700 rounded-lg text-white placeholder-gray-400"
            />
            <div className="flex items-center space-x-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setCurrentRating(prev => ({ ...prev, rating: star }))}
                  className={`p-1 ${currentRating.rating >= star ? 'text-purple-500' : 'text-gray-600'}`}
                >
                  <Star className="h-6 w-6" fill={currentRating.rating >= star ? 'currentColor' : 'none'} />
                </button>
              ))}
            </div>
            <textarea
              placeholder="Write your review (keep it friendly and appropriate)"
              value={currentRating.review}
              onChange={(e) => setCurrentRating(prev => ({ ...prev, review: e.target.value }))}
              className="w-full px-4 py-2 bg-gray-800 border-gray-700 rounded-lg text-white placeholder-gray-400 h-32 resize-none"
            />
            <div className="flex space-x-2">
              <button
                onClick={handleRatingSubmit}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              >
                Submit Review
              </button>
              <button
                onClick={() => setShowRatingModal(false)}
                className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700"
              >
                Cancel
              </button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const LanguageSelector = () => (
    <select
      value={selectedLanguage}
      onChange={(e) => setSelectedLanguage(e.target.value)}
      className="px-3 py-1 bg-gray-800 border-gray-700 rounded-lg text-sm text-gray-300"
    >
      {languages.map((lang) => (
        <option key={lang.code} value={lang.code} className="bg-gray-800">
          {lang.name}
        </option>
      ))}
    </select>
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    setTimeout(() => {
      const response = `Here's what I found about "${inputMessage}". You can rate this content using the rate button below.`;
      const translatedResponse = selectedLanguage === 'en' ? response :
        `[Translated to ${languages.find(l => l.code === selectedLanguage)?.name}]: ${response}`;

      setMessages(prev => [...prev, {
        type: 'bot',
        content: translatedResponse,
        timestamp: new Date(),
        originalLanguage: 'en',
        translatedTo: selectedLanguage
      }]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div
      ref={resizeRef}
      className={`fixed transition-all duration-75 ease-in-out ${
        isMinimized ? 'bottom-4 right-4 w-64 h-12' : ''
      }`}
      style={{
        position: 'fixed',
        right: position.x !== 'auto' ? `${position.x}px` : '1rem',
        bottom: position.y !== 'auto' ? `${position.y}px` : '1rem',
        width: isMinimized ? '256px' : `${dimensions.width}px`,
        height: isMinimized ? '48px' : `${dimensions.height}px`,
        zIndex: 50
      }}
    >
      <Card className="w-full h-full flex flex-col bg-gray-900 border-gray-700 shadow-xl rounded-lg overflow-hidden relative">
        {/* Header */}
        <div
          className="border-b border-gray-700 bg-gray-900 p-4 flex items-center justify-between cursor-move select-none"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget || e.target.parentElement === e.currentTarget) {
              setIsDragging(true);
              dragRef.current = e.currentTarget;
            }
          }}
        >
          <div className="flex items-center space-x-2">
            <Bot className="h-6 w-6 text-purple-500" />
            <div>
              <h2 className="font-semibold text-white">Entertainment AI Assistant</h2>
              {!isMinimized && (
                <p className="text-xs text-gray-400">Powered by RAG technology</p>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {!isMinimized && (
              <div className="flex items-center space-x-2">
                <Globe className="h-4 w-4 text-gray-400" />
                <LanguageSelector />
              </div>
            )}
            <div className="flex items-center space-x-2">
              {isMinimized ? (
                <button
                  onClick={() => setIsMinimized(false)}
                  className="p-1 hover:bg-gray-800 rounded"
                >
                  <Maximize className="h-4 w-4 text-gray-400" />
                </button>
              ) : (
                <>
                  <button
                    onClick={() => setIsMinimized(true)}
                    className="p-1 hover:bg-gray-800 rounded"
                  >
                    <Minimize className="h-4 w-4 text-gray-400" />
                  </button>
                  <button
                    onClick={() => setIsMinimized(true)}
                    className="p-1 hover:bg-gray-800 rounded"
                  >
                    <X className="h-4 w-4 text-gray-400" />
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Expandable content */}
        {!isMinimized && (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex space-x-2 max-w-[80%] ${
                    message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
                  }`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === 'user' ? 'bg-purple-900' : 'bg-gray-800'
                    }`}>
                      {message.type === 'user' ? (
                        <User className="h-5 w-5 text-purple-400" />
                      ) : (
                        <Bot className="h-5 w-5 text-gray-400" />
                      )}
                    </div>
                    <div className={`rounded-lg p-3 ${
                      message.isError ? 'bg-red-900/50 text-red-300' :
                      message.type === 'user' ? 'bg-purple-600 text-white' : 'bg-gray-800 text-gray-200'
                    }`}>
                      {message.content}
                      <div className="text-xs mt-1 text-gray-400">
                        {message.timestamp.toLocaleTimeString()}
                        {message.translatedTo && message.translatedTo !== 'en' && (
                          <span className="ml-2">
                            <Globe className="h-3 w-3 inline mr-1" />
                            Translated
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center">
                    <Bot className="h-5 w-5 text-gray-400" />
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 flex items-center space-x-2">
                    <Loader className="h-4 w-4 animate-spin text-purple-500" />
                    <span className="text-sm text-gray-300">Thinking...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Ask about movies, shows, actors, or directors..."
                  className="flex-1 px-4 py-2 bg-gray-800 border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  type="button"
                  onClick={() => setShowRatingModal(true)}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  <Star className="h-5 w-5" />
                </button>
                <button
                  type="submit"
                  disabled={!inputMessage.trim() || isTyping}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </form>

            {/* Resize handles */}
            <div
              className="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize group"
              onMouseDown={(e) => startResize(e, 'se')}
            >
              <div className="absolute bottom-1 right-1 w-2 h-2 bg-gray-500 group-hover:bg-purple-500 rounded-sm transition-colors"></div>
            </div>
            <div
              className="absolute bottom-0 right-4 left-0 h-1 cursor-s-resize hover:bg-purple-500/20"
              onMouseDown={(e) => startResize(e, 's')}
            ></div>
            <div
              className="absolute bottom-4 right-0 w-1 top-0 cursor-e-resize hover:bg-purple-500/20"
              onMouseDown={(e) => startResize(e, 'e')}
            ></div>
          </>
        )}
      </Card>

      {showRatingModal && <RatingModal />}
    </div>
  );
};

export default FloatingRAGChatbot;