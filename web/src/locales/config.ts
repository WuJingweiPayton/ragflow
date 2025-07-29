import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { initReactI18next } from 'react-i18next';

import { LanguageAbbreviation } from '@/constants/common';
import translation_en from './en';
import { createTranslationTable, flattenObject } from './until';
import translation_zh from './zh';

const resources = {
  [LanguageAbbreviation.En]: translation_en,
  [LanguageAbbreviation.Zh]: translation_zh,
};
const enFlattened = flattenObject(translation_en);
const zhFlattened = flattenObject(translation_zh);
export const translationTable = createTranslationTable(
  [
    enFlattened,
    zhFlattened,
  ],
  [
    'English',
    '简体中文',
  ],
);
i18n
  .use(initReactI18next)
  .use(LanguageDetector)
  .init({
    detection: {
      lookupLocalStorage: 'lng',
    },
    supportedLngs: Object.values(LanguageAbbreviation),
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
