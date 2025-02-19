import { useState, useCallback } from 'react';
import { translations } from '../i18n/translations';

type Language = 'en' | 'es' | 'fr' | 'de' | 'pt' | 'jp';

export function useTranslation() {
  const [currentLanguage, setCurrentLanguage] = useState<Language>('en');

  const t = useCallback((key: keyof typeof translations['en']) => {
    return translations[currentLanguage][key];
  }, [currentLanguage]);

  return {
    t,
    currentLanguage,
    setLanguage: setCurrentLanguage,
    availableLanguages: [
      { code: 'en', name: 'English' },
      { code: 'es', name: 'Español' },
      { code: 'fr', name: 'Français' },
      { code: 'de', name: 'Deutsch' },
      { code: 'pt', name: 'Português' },
      { code: 'jp', name: '日本語' }
    ]
  };
}