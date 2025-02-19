// src/components/ChatbotTrigger.tsx
import React, { useState } from 'react';
import { MessageSquare, X } from 'lucide-react';
import FloatingRAGChatbot from './FloatingRAGChatbot';

const ChatbotTrigger = ({ t }) => {
  const [showChatbot, setShowChatbot] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const toggleChatbot = () => {
    setShowChatbot(prev => !prev);
  };

  return (
    <>
      <button
        onClick={toggleChatbot}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="group relative flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-full transition-all duration-200 ease-in-out shadow-lg hover:shadow-purple-500/25"
      >
        <div className="flex items-center space-x-2">
          {showChatbot ? (
            <X size={16} className="transition-transform duration-200 group-hover:rotate-90" />
          ) : (
            <MessageSquare
              size={16}
              className={`transition-transform duration-200 ${
                isHovered ? 'scale-110' : 'scale-100'
              }`}
            />
          )}
          <span className="text-sm font-medium whitespace-nowrap">
            {showChatbot ? t('closeChat') : t('askChatbot')}
          </span>
        </div>

        {showChatbot && (
          <span className="absolute right-0 top-0 flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-300 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-purple-400"></span>
          </span>
        )}
      </button>

      {showChatbot && (
        <FloatingRAGChatbot
          onClose={() => setShowChatbot(false)}
          initiallyMinimized={false}
        />
      )}
    </>
  );
};

export default ChatbotTrigger;