export default {
  general: {
    submit: 'Отправить',
    create: 'Создать',
    delete: 'Удалить',
    cancel: 'Отмена',

    pageNotFound: 'Страница не найдена',

    copyLink: 'Ссылка',
    linkCopied: 'Ссылка скопирована',
    downloadTable: 'Скачать таблицу',

    min: 'мин. {n}',
    max: 'макс. {n}',
    fromAToB: 'от {a} до {b}',

    maxChar: '@:general.max симв.',

    overview: 'Общий вид',
    at: 'в',
    view: 'Посмотреть',

    irreversible: 'Это действие необратимо',
  },
  profile: {
    profile: 'Профиль',
  },
  forms: {
    form: 'Форма',
    forms: 'Формы',
    question: 'Вопрос',
    submission: 'Ответ',
    answers: 'Ответы',
    questionsNumber: '0 вопросов | {n} вопрос | {n} вопроса | {n} вопросов',
    submissionsNumber: '0 ответов | {n} ответ | {n} ответа | {n} ответов',
    answersNumber: 'нет ответов | {n} ответ | {n} ответа | {n} ответов',
    active: 'Активна',
    closed: 'Закрыта',

    close: 'Закрыть',
    closeForm: 'Закрыть форму',
    closeFormConfirm: 'Вы уверены, что хотите закрыть эту форму? Новые ответы будут невозможны.',

    closedMessage: 'Эта форма закрыта. Новые ответы невозможны.',

    title: 'Название',
    description: 'Описание',
    required: 'обязательный',
    notRequired: 'не обязательный',
    selectQuestionType: 'Выберите тип вопроса',

    types: {
      text: 'Текст',
      number: 'Число',
      color: 'Цвет',
      choice: 'Выбор из вариантов'
    },

    choices: {
      variant: 'Вариант ответа',
      addVariant: 'Добавить вариант ответа',
    },

    restrictionsLabel: 'Ограничения',

    addQuestion: 'Добавить вопрос',
    delete: 'Удалить форму',

    confirmDelete: 'Вы уверены что хотите удалить эту форму? Вы потеряете все ответы. Возможно, вы хотите закрыть её?',

    formSuccessfullyCreated: 'Форма была успешно создана!',
    nowYouCanShareViaLink: 'Теперь вы можете поделиться ей с помощью ссылки',

    formSuccessfullySubmitted: 'Ответ был успешно отправлен!',

    restrictions: {
      maxAnswerLength: 'Макс. длина ответа',
      maxValue: 'Макс. значение',
      minValue: 'Мин. значение',
      numericAnswerType: 'Тип ответа',
      canBeFloat: 'Может быть нецелым числом',
      regex: 'Регулярное выражение',
    },

    byQuestions: 'По вопросам',
    bySubmissions: 'По ответам',
    
    noAnswer: 'без ответа',

    averageValue: 'Среднее значение',
  },
  placeholders: {
    number: 'число',
    regex: "\\d*"
  },
  auth: {
    login: 'Вход',
    loginButton: 'Войти',
    register: 'Регистрация',
    registerButton: 'Зарегистрироваться',
    username: 'имя пользователя',
    password: 'пароль',
    confirmPassword: 'пароль повторно',
    logout: 'Выйти',

    enterPassword: 'Введите пароль',
    weakPassword: 'Слишком слабый',
    mediumPassword: 'Средний',
    strongPassword: 'Отличный!',
  },
  landing: {
    title: {
      creating: 'Создавать',
      forms: 'Формы',
      hasNeverBeenThatEasy: 'ещё никогда не было так легко!',
    },
    features: {
      features: 'Features',
      first: {
        title: 'Гибкая настройка ограничений',
        text: 'Ограничивайте текстовые ответы регулярными выражениями (RegExp) и устанавливайте макс. длину. Для числовых ответов вы можете установить мин. и макс. значения',
      },
      second: {
        title: 'Получайте уведомления о новых ответах',
        text: 'Подключите нашего Telegram бота и получайте уведомления о каждом заполнении формы',
      },
      third: {
        title: 'Экспортируйте все ответы в Excel-таблицу',
        text: 'Вы легко можете экспортировать все ответы на форму в универсальном формате',
      },
    }
  },
}