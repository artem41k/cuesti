import { createI18n } from "vue-i18n";
import en from "./locales/en";
import ru from "./locales/ru";


const customPluralization = (choice, choicesLength, orgRule) => {
  if (choice === 0) {
    return 0
  }

  const teen = choice > 10 && choice < 20
  const endsWithOne = choice % 10 === 1
  if (!teen && endsWithOne) {
    return 1
  }
  if (!teen && choice % 10 >= 2 && choice % 10 <= 4) {
    return 2
  }

  return choicesLength < 4 ? 2 : 3
}


export const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  pluralizationRules: {
    ru: customPluralization
  },
  messages: {
    en,
    ru
  }
})