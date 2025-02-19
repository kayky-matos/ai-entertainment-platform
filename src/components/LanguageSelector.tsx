import React from 'react';
import { Globe } from 'lucide-react';

type Language = {
  code: string;
  name: string;
};

interface LanguageSelectorProps {
  currentLanguage: string;
  languages: Language[];
  onLanguageChange: (code: string) => void;
}

export function LanguageSelector({ currentLanguage, languages, onLanguageChange }: LanguageSelectorProps) {
  return (
    <div className="relative group">
      <button className="flex items-center space-x-2 px-3 py-1 bg-[#2a2d34] rounded-lg text-gray-300 hover:text-white">
        <Globe size={16} />
        <span className="text-sm">{languages.find(lang => lang.code === currentLanguage)?.name}</span>
      </button>
      <div className="absolute right-0 mt-2 w-40 py-2 bg-[#1a1d24] rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
        {languages.map((language) => (
          <button
            key={language.code}
            onClick={() => onLanguageChange(language.code)}
            className={`w-full px-4 py-2 text-left text-sm hover:bg-[#2a2d34] transition-colors ${
              currentLanguage === language.code ? 'text-purple-500' : 'text-gray-300'
            }`}
          >
            {language.name}
          </button>
        ))}
      </div>
    </div>
  );
}